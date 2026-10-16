-- Execute this file as one SQL statement after 20261007_needs_assessment.sql.
-- REPORT_MEDIA already exists; this adds the photo category and precise edit version.
ALTER TABLE REPORT_MEDIA
    ADD COLUMN media_group VARCHAR(64) NULL AFTER media_type,
    MODIFY COLUMN updated_at DATETIME(6) NOT NULL
        DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
