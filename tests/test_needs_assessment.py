import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

from src.dto.report_sync_dto import ReportSyncDTO
from src.dto.report_reference_dto import ReportReferenceDTO
from src.dto.attachment_dto import MediaFinalizeItemDTO, MediaVersionDTO
from src.service.report_service import ReportService
from src.service.ordem_service_attachment import OrdemServiceAttachmentService


class FakeConnection:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class NeedsAssessmentTests(unittest.TestCase):
    def test_media_groups_and_object_keys(self):
        service = object.__new__(OrdemServiceAttachmentService)
        photo = SimpleNamespace(
            id='photo-1', type='photo', group='external_compressor',
            content_type='image/jpeg',
        )
        service._validate_media([photo], 'NEEDS_ASSESSMENT')
        self.assertEqual(
            service._object_key('client', 'assessment', photo, 'NEEDS_ASSESSMENT'),
            'clients/client/reports/assessment/needs-assessment/external_compressor/photo-1.jpg',
        )
        with self.assertRaises(ValueError):
            service._validate_media([SimpleNamespace(**{**vars(photo), 'group': '../outside'})], 'NEEDS_ASSESSMENT')
        with self.assertRaises(ValueError):
            service._validate_media([SimpleNamespace(**{**vars(photo), 'type': 'signature'})], 'NEEDS_ASSESSMENT')
        legacy = SimpleNamespace(id='old', type='photo', group=None, content_type='image/png')
        self.assertEqual(
            service._object_key('client', 'order', legacy, 'ORDEM_SERVICE'),
            'clients/client/reports/order/photos/old.jpg',
        )

    def test_stale_answers_are_rejected_without_overwrite(self):
        service = object.__new__(ReportService)
        service.report_repository = SimpleNamespace(
            get_by_id_reference_and_id_client=lambda *_: SimpleNamespace(
                type='NEEDS_ASSESSMENT', id_reference='n1'
            ),
        )
        service.needs_repository = SimpleNamespace(
            get_by_id=lambda *_args, **_kwargs: {
                'id_company': 'c1', 'updated_at': datetime(2026, 10, 7, 12, 0, 1)
            },
            upsert=lambda *_: self.fail('stale payload must not be saved'),
        )
        connection = FakeConnection()
        dto = ReportReferenceDTO(id='n1', needs_assessment={
            'id_company': 'c1', 'base_updated_at': '2026-10-07T12:00:00',
        })
        with patch('src.service.report_service.get_connection', return_value=connection):
            result, status = service.update_reference(dto, 'user', 'client')
        self.assertEqual(status, 409)
        self.assertTrue(connection.closed)
        self.assertIn('outro aparelho', result['message'])

    def test_stale_media_manifest_is_rejected(self):
        service = object.__new__(OrdemServiceAttachmentService)
        service._get_owned_report = lambda *_: SimpleNamespace(type='NEEDS_ASSESSMENT')
        service.s3 = SimpleNamespace(head_object=lambda **_: {})
        service.bucket_name = 'bucket'
        service.media_repository = SimpleNamespace(
            lock_report=lambda *_: None,
            get_report_media=lambda *_: [{
                'id': 'photo-1',
                'object_key': 'clients/client/reports/n1/needs-assessment/external_compressor/photo-1.jpg',
                'updated_at': datetime(2026, 10, 7, 12, 0, 1),
            }],
            foreign_media_ids=lambda *_: [],
            replace_report_media=lambda *_: self.fail('stale media must not be saved'),
        )
        item = MediaFinalizeItemDTO(
            id='photo-1', type='photo', group='external_compressor',
            content_type='image/jpeg', size_bytes=10,
            object_key='clients/client/reports/n1/needs-assessment/external_compressor/photo-1.jpg',
        )
        base = MediaVersionDTO(id='photo-1', object_key=item.object_key, updated_at='2026-10-07T12:00:00')
        connection = FakeConnection()
        with patch('src.service.ordem_service_attachment.get_connection', return_value=connection):
            result, status = service.finalize('n1', 'client', [item], [base])
        self.assertEqual(status, 409)
        self.assertTrue(connection.closed)
        self.assertIn('outro aparelho', result['message'])

    def test_unchanged_photo_does_not_repeat_bucket_head(self):
        service = object.__new__(OrdemServiceAttachmentService)
        service._get_owned_report = lambda *_: SimpleNamespace(type='NEEDS_ASSESSMENT')
        service.s3 = SimpleNamespace(head_object=lambda **_: self.fail('existing photo needs no HEAD'))
        service.bucket_name = 'bucket'
        key = 'clients/client/reports/n1/needs-assessment/air_filter/photo-1.jpg'
        version = datetime(2026, 10, 7, 12, 0, 1)
        service.media_repository = SimpleNamespace(
            lock_report=lambda *_: None,
            get_report_media=lambda *_: [{'id': 'photo-1', 'object_key': key, 'updated_at': version}],
            foreign_media_ids=lambda *_: [],
            replace_report_media=lambda *_: None,
            get_manifests=lambda *_: {'n1': [{'id': 'photo-1', 'object_key': key}]},
        )
        item = MediaFinalizeItemDTO(
            id='photo-1', type='photo', group='air_filter',
            content_type='image/jpeg', size_bytes=10, object_key=key,
        )
        base = MediaVersionDTO(id='photo-1', object_key=key, updated_at=version.isoformat())
        connection = FakeConnection()
        with patch('src.service.ordem_service_attachment.get_connection', return_value=connection):
            result, status = service.finalize('n1', 'client', [item], [base])
        self.assertEqual(status, 200)
        self.assertTrue(result['success'])
        self.assertTrue(connection.closed)

    def test_mixed_sync_keeps_page_order_and_media_groups(self):
        service = object.__new__(ReportService)
        page = [
            {'id': 'r1', 'id_reference': 'o1', 'type': 'ORDEM_SERVICE', 'created_at': None, 'updated_at': None},
            {'id': 'r2', 'id_reference': 'n1', 'type': 'NEEDS_ASSESSMENT', 'created_at': None, 'updated_at': None},
        ]
        service.report_repository = SimpleNamespace(
            get_report_sync_total=lambda *_: 2,
            get_report_sync_page=lambda *_: page,
            get_ordem_services_by_report_ids=lambda *_: [
                {'report_id': 'r1', 'id': 'o1', 'company_id': 'c1', 'company_name': 'Cliente',
                 'equipament_id': 'e1', 'equipament_name': 'Compressor'},
            ],
        )
        service.needs_repository = SimpleNamespace(get_by_report_ids=lambda *_: [
            {'report_id': 'r2', 'id': 'n1', 'id_company': 'c1', 'id_equipament': 'e1',
             'air_filter': 1, 'company_id': 'c1', 'company_name': 'Cliente',
             'equipament_id': 'e1', 'equipament_name': 'Compressor'},
        ])
        service.media_repository = SimpleNamespace(get_manifests=lambda *_: {
            'n1': [{'id': 'photo-1', 'group': 'air_filter', 'type': 'photo'}],
        })
        connection = FakeConnection()
        with patch('src.service.report_service.get_connection', return_value=connection):
            result, status = service.get_report_sync(ReportSyncDTO(page=1, limit=10), 'client')
        self.assertEqual(status, 200)
        self.assertTrue(connection.closed)
        self.assertEqual([item['report']['id'] for item in result['data']], ['r1', 'r2'])
        self.assertEqual(result['data'][0]['ordem_service']['company']['name'], 'Cliente')
        self.assertTrue(result['data'][1]['needs_assessment']['air_filter'])
        self.assertEqual(result['data'][1]['media_manifest'][0]['group'], 'air_filter')


if __name__ == '__main__':
    unittest.main()
