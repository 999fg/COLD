use CS408;
CREATE TABLE file (
    file_name VARCHAR(255) NOT NULL,
    file_block_name VARCHAR(255) NOT NULL,
    file_block_index INT(10) NOT NULL,
    saved_device_address VARCHAR(255) NOT NULL,
    file_size BIGINT(20) NOT NULL,
    block_size BIGINT(20) NOT NULL,
    PRIMARY KEY (file_name, file_block_name, file_block_index, saved_device_address)
);
