CREATE TABLE IF NOT EXISTS REPORT_MEDIA (
    id VARCHAR(36) NOT NULL,
    report_reference_id VARCHAR(36) NOT NULL,
    media_type ENUM('photo', 'signature') NOT NULL,
    object_key VARCHAR(512) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    size_bytes BIGINT UNSIGNED NOT NULL,
    note TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_report_media_object_key (object_key),
    KEY idx_report_media_reference (report_reference_id)
);
