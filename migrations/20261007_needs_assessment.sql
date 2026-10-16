-- Execute this file as one SQL statement in DBeaver.
-- IDs are validated against COMPANY and EQUIPAMENT by the API.
-- The existing COMPANY.id is not a standalone unique key, so no FK is declared.
CREATE TABLE IF NOT EXISTS NEEDS_ASSESSMENT (
    id CHAR(36) NOT NULL,
    id_company CHAR(36) NOT NULL,
    id_equipament CHAR(36) NULL,
    external_compressor_notes TEXT NULL,
    internal_compressor_notes TEXT NULL,
    air_filter TINYINT(1) NULL,
    oil_filter TINYINT(1) NULL,
    air_oil_separator TINYINT(1) NULL,
    pre_coalescing TINYINT(1) NULL,
    post_coalescing TINYINT(1) NULL,
    belts TINYINT(1) NULL,
    hoses TINYINT(1) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    KEY idx_needs_company (id_company),
    KEY idx_needs_equipament (id_equipament)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
