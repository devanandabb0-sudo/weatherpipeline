CREATE OR REPLACE TABLE weather_data (
    city STRING,
    temperature FLOAT,
    humidity FLOAT,
    weather STRING,
    timestamp STRING
);

CREATE OR REPLACE FILE FORMAT json_format
TYPE = 'JSON';


CREATE OR REPLACE STAGE weather_stage
URL = 's3://weather-bucket-200/'
STORAGE_INTEGRATION = s3_int
FILE_FORMAT = (TYPE = JSON);


-- Snowpipe (AUTO LOAD)
CREATE OR REPLACE PIPE weather_pipe
AUTO_INGEST = TRUE
AS
COPY INTO weather_data
FROM (
  SELECT
    $1:city::STRING,
    $1:temperature::FLOAT,
    $1:humidity::FLOAT,
    $1:weather::STRING,
    $1:timestamp::STRING
  FROM @weather_stage
);