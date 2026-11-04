-- Apply this migration manually in the target database.
-- It is intentionally not executed by the application.

CREATE TABLE IF NOT EXISTS COMPANY_CONTACT (
    id VARCHAR(36) NOT NULL,
    company_id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NULL,
    phone VARCHAR(50) NULL,
    signature_object_key VARCHAR(512) NULL,
    signature_content_type VARCHAR(100) NULL,
    signature_size_bytes BIGINT UNSIGNED NULL,
    signature_updated_at DATETIME NULL,
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_company_contact_company (company_id),
    KEY idx_company_contact_active (company_id, deleted_at)
);

ALTER TABLE ORDEM_SERVICE
    ADD COLUMN closing_contact_id VARCHAR(36) NULL AFTER closing_responsible;

CREATE INDEX idx_ordem_service_closing_contact ON ORDEM_SERVICE (closing_contact_id);
