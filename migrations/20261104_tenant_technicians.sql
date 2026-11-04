-- Apply manually. This migration is never run by the application.
CREATE TABLE IF NOT EXISTS TENANT_TECHNICIAN (
    id VARCHAR(36) NOT NULL, client_id VARCHAR(36) NOT NULL, name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NULL, phone VARCHAR(50) NULL, signature_object_key VARCHAR(512) NULL,
    signature_content_type VARCHAR(100) NULL, signature_size_bytes BIGINT UNSIGNED NULL,
    signature_updated_at DATETIME NULL, deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), KEY idx_tenant_technician_active (client_id, deleted_at)
);
CREATE TABLE IF NOT EXISTS ORDEM_SERVICE_TECHNICIAN (
    order_service_id VARCHAR(36) NOT NULL, technician_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (order_service_id, technician_id), KEY idx_os_technician_technician (technician_id)
);
