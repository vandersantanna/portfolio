<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# 🔷 SQL Server Performance Engineering Guide
*DMVs, Query Store, and wait stats to diagnose, fix, and verify—on-prem and cloud.*


## 📋 Table of Contents

- [🎯 Objectives](#-objectives)
- [🔐 Required Permissions](#-required-permissions)
- [🔍 Performance Analysis](#-performance-analysis)
- [📊 SQL Server Index Types](#-sql-server-index-types)
- [⚙️ Parameter Configuration](#️-parameter-configuration)
- [🖥️ On-Premise Tuning](#️-on-premise-tuning)
- [☁️ Cloud Tuning](#️-cloud-tuning)
- [🔧 Specialized Tools](#-specialized-tools)
- [💼 Practical Cases](#-practical-cases)
- [📊 Automated Monitoring](#-automated-monitoring)
- [🛠️ Management Tools](#️-management-tools)

---

## 🎯 Objectives

> **Expert-level SQL Server performance optimization for mission-critical production environments**, including advanced configuration, query analysis, index tuning, and scalable solutions implementation across on-premise and cloud platforms.

### Performance Targets
- **Latency**: < 50ms for 95% of queries
- **Throughput**: > 15,000 TPS (Transactions Per Second)
- **Availability**: 99.9% uptime
- **Buffer Cache Hit Ratio**: > 99%
- **Page Life Expectancy**: > 300 seconds

### Key Performance Indicators (KPIs)
```sql
-- Main KPIs for SQL Server monitoring
SELECT 
    'Buffer Cache Hit Ratio' as metric,
    CAST((cntr_value * 100.0 / 
        (SELECT cntr_value FROM sys.dm_os_performance_counters 
         WHERE counter_name = 'Buffer cache hit ratio base')) AS DECIMAL(5,2)) as hit_ratio
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Buffer cache hit ratio'
AND object_name LIKE '%Buffer Manager%'

UNION ALL

SELECT 
    'Page Life Expectancy' as metric,
    cntr_value as seconds
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Page life expectancy'
AND object_name LIKE '%Buffer Manager%'

UNION ALL

SELECT 
    'Batch Requests/sec' as metric,
    cntr_value as requests_per_sec
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Batch Requests/sec';
```

[Back to top](#table-of-contents)

---

## 🔐 Required Permissions

### Monitoring User Setup
```sql
-- Create specific user for monitoring
CREATE LOGIN [monitoring_user] WITH PASSWORD = 'SecurePassword123!';
GO

USE [your_database];
CREATE USER [monitoring_user] FOR LOGIN [monitoring_user];

-- Grant necessary permissions
GRANT VIEW SERVER STATE TO [monitoring_user];
GRANT VIEW DATABASE STATE TO [monitoring_user];
GRANT SELECT ON sys.dm_exec_requests TO [monitoring_user];
GRANT SELECT ON sys.dm_exec_sessions TO [monitoring_user];
GRANT SELECT ON sys.dm_os_performance_counters TO [monitoring_user];

-- Query Store permissions
ALTER ROLE [db_datareader] ADD MEMBER [monitoring_user];
```
[Back to top](#table-of-contents)

---
## 🔍 Performance Analysis

### Top Slow Queries Analysis
```sql
-- Top 20 slowest queries by average CPU time
SELECT TOP 20
    qs.sql_handle,
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count AS avg_elapsed_time,
    qs.total_worker_time / qs.execution_count AS avg_cpu_time,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    SUBSTRING(st.text, (qs.statement_start_offset/2)+1, 
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(st.text)
            ELSE qs.statement_end_offset
        END - qs.statement_start_offset)/2) + 1) AS statement_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
WHERE qs.execution_count > 10
ORDER BY avg_cpu_time DESC;
```

### Wait Statistics Analysis
```sql
-- Wait statistics analysis
WITH Waits AS (
    SELECT 
        wait_type,
        wait_time_ms / 1000.0 AS WaitS,
        (wait_time_ms - signal_wait_time_ms) / 1000.0 AS ResourceS,
        signal_wait_time_ms / 1000.0 AS SignalS,
        waiting_tasks_count AS WaitCount,
        100.0 * wait_time_ms / SUM (wait_time_ms) OVER() AS Percentage,
        ROW_NUMBER() OVER(ORDER BY wait_time_ms DESC) AS RowNum
    FROM sys.dm_os_wait_stats 
    WHERE wait_type NOT IN (
        N'BROKER_EVENTHANDLER', N'BROKER_RECEIVE_WAITFOR',
        N'BROKER_TASK_STOP', N'BROKER_TO_FLUSH',
        N'BROKER_TRANSMITTER', N'CHECKPOINT_QUEUE',
        N'CHKPT', N'CLR_AUTO_EVENT', N'CLR_MANUAL_EVENT',
        N'CLR_SEMAPHORE', N'DBMIRROR_DBM_EVENT',
        N'DBMIRROR_EVENTS_QUEUE', N'DBMIRROR_WORKER_QUEUE',
        N'DBMIRRORING_CMD', N'DIRTY_PAGE_POLL', N'DISPATCHER_QUEUE_SEMAPHORE',
        N'EXECSYNC', N'FSAGENT', N'FT_IFTS_SCHEDULER_IDLE_WAIT',
        N'FT_IFTSHC_MUTEX', N'HADR_CLUSAPI_CALL',
        N'HADR_FILESTREAM_IOMGR_IOCOMPLETION', N'HADR_LOGCAPTURE_WAIT',
        N'HADR_NOTIFICATION_DEQUEUE', N'HADR_TIMER_TASK',
        N'HADR_WORK_QUEUE', N'KSOURCE_WAKEUP',
        N'LAZYWRITER_SLEEP', N'LOGMGR_QUEUE',
        N'MEMORY_ALLOCATION_EXT', N'ONDEMAND_TASK_QUEUE',
        N'PREEMPTIVE_XE_GETTARGETSTATE', N'PWAIT_ALL_COMPONENTS_INITIALIZED',
        N'PWAIT_DIRECTLOGCONSUMER_GETNEXT', N'QDS_PERSIST_TASK_MAIN_LOOP_SLEEP',
        N'QDS_ASYNC_QUEUE', N'QDS_CLEANUP_STALE_QUERIES_TASK_MAIN_LOOP_SLEEP',
        N'QDS_SHUTDOWN_QUEUE', N'REDO_THREAD_PENDING_WORK',
        N'REQUEST_FOR_DEADLOCK_SEARCH', N'RESOURCE_QUEUE',
        N'SERVER_IDLE_CHECK', N'SLEEP_BPOOL_FLUSH',
        N'SLEEP_DBSTARTUP', N'SLEEP_DCOMSTARTUP',
        N'SLEEP_MASTERDBREADY', N'SLEEP_MASTERMDREADY',
        N'SLEEP_MASTERUPGRADED', N'SLEEP_MSDBSTARTUP',
        N'SLEEP_SYSTEMTASK', N'SLEEP_TASK', N'SLEEP_TEMPDBSTARTUP',
        N'SNI_HTTP_ACCEPT', N'SP_SERVER_DIAGNOSTICS_SLEEP',
        N'SQLTRACE_BUFFER_FLUSH', N'SQLTRACE_INCREMENTAL_FLUSH_SLEEP',
        N'SQLTRACE_WAIT_ENTRIES', N'WAIT_FOR_RESULTS',
        N'WAITFOR', N'WAITFOR_TASKSHUTDOWN', N'WAIT_XTP_RECOVERY',
        N'WAIT_XTP_HOST_WAIT', N'WAIT_XTP_OFFLINE_CKPT_NEW_LOG',
        N'WAIT_XTP_CKPT_CLOSE', N'XE_DISPATCHER_JOIN',
        N'XE_DISPATCHER_WAIT', N'XE_LIVE_TARGET_TVF',
        N'XE_TIMER_EVENT'
    )
    AND waiting_tasks_count > 0
)
SELECT
    W1.wait_type AS [WaitType], 
    CAST (W1.WaitS AS DECIMAL (16, 2)) AS [Wait_S],
    CAST (W1.ResourceS AS DECIMAL (16, 2)) AS [Resource_S],
    CAST (W1.SignalS AS DECIMAL (16, 2)) AS [Signal_S],
    W1.WaitCount AS [WaitCount],
    CAST (W1.Percentage AS DECIMAL (5, 2)) AS [Percentage],
    CAST ((W1.WaitS / W1.WaitCount) AS DECIMAL (16, 4)) AS [AvgWait_S],
    CAST ((W1.ResourceS / W1.WaitCount) AS DECIMAL (16, 4)) AS [AvgRes_S],
    CAST ((W1.SignalS / W1.WaitCount) AS DECIMAL (16, 4)) AS [AvgSig_S]
FROM Waits AS W1 
INNER JOIN Waits AS W2 ON W2.RowNum <= W1.RowNum 
GROUP BY W1.RowNum, W1.wait_type, W1.WaitS, W1.ResourceS, W1.SignalS, 
         W1.WaitCount, W1.Percentage 
HAVING SUM (W2.Percentage) - W1.Percentage < 95
ORDER BY W1.RowNum;
```

### Missing Indexes Analysis
```sql
-- Missing indexes analysis
SELECT 
    migs.avg_total_user_cost * (migs.avg_user_impact / 100.0) * (migs.user_seeks + migs.user_scans) AS improvement_measure,
    'CREATE INDEX [IX_' + OBJECT_NAME(mid.object_id, mid.database_id) + '_'
    + REPLACE(REPLACE(REPLACE(ISNULL(mid.equality_columns,''), ', ', '_'), '[', ''), ']', '') +
    CASE
        WHEN mid.inequality_columns IS NOT NULL THEN '_' + REPLACE(REPLACE(REPLACE(mid.inequality_columns, ', ', '_'), '[', ''), ']', '')
        ELSE ''
    END + '] ON ' + mid.statement
    + ' (' + ISNULL (mid.equality_columns,'')
    + CASE WHEN mid.equality_columns IS NOT NULL AND mid.inequality_columns IS NOT NULL THEN ',' ELSE '' END
    + ISNULL (mid.inequality_columns, '')
    + ')'
    + ISNULL (' INCLUDE (' + mid.included_columns + ')', '') AS create_index_statement,
    migs.*,
    mid.database_id,
    mid.[object_id]
FROM sys.dm_db_missing_index_groups mig
INNER JOIN sys.dm_db_missing_index_group_stats migs ON migs.group_handle = mig.index_group_handle
INNER JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE migs.avg_total_user_cost * (migs.avg_user_impact / 100.0) * (migs.user_seeks + migs.user_scans) > 10
ORDER BY migs.avg_total_user_cost * migs.avg_user_impact * (migs.user_seeks + migs.user_scans) DESC;
```

### Resource Usage Analysis
```sql
-- CPU and memory usage by database
SELECT 
    DB_NAME(database_id) AS DatabaseName,
    SUM(total_worker_time) AS CPU_Time_Ms,
    SUM(total_physical_reads) AS Physical_Reads,
    SUM(total_logical_reads) AS Logical_Reads,
    SUM(total_logical_writes) AS Logical_Writes,
    COUNT(*) AS Query_Count
FROM sys.dm_exec_query_stats qs
CROSS APPLY (SELECT CONVERT(int, value) AS database_id 
             FROM sys.dm_exec_plan_attributes(qs.plan_handle)
             WHERE attribute = N'dbid') AS F_DB
WHERE database_id > 4 -- Exclude system databases for this analysis
GROUP BY database_id
ORDER BY CPU_Time_Ms DESC;
```

### Index Usage Statistics
```sql
-- Index usage statistics
SELECT 
    OBJECT_NAME(ius.object_id) AS TableName,
    i.name AS IndexName,
    i.type_desc AS IndexType,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    ius.user_updates,
    ius.user_seeks + ius.user_scans + ius.user_lookups AS total_reads,
    CASE 
        WHEN ius.user_updates > 0 
        THEN CAST((ius.user_seeks + ius.user_scans + ius.user_lookups) AS FLOAT) / ius.user_updates
        ELSE NULL
    END AS reads_per_update
FROM sys.dm_db_index_usage_stats ius
INNER JOIN sys.indexes i ON ius.object_id = i.object_id AND ius.index_id = i.index_id
WHERE ius.database_id = DB_ID()
    AND OBJECT_NAME(ius.object_id) NOT LIKE 'sys%'
ORDER BY total_reads DESC;
```

### Query Execution Plans Analysis
```sql
-- Most expensive queries by I/O
SELECT TOP 20
    qs.total_logical_reads,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.total_physical_reads,
    qs.total_worker_time,
    qs.total_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, qs.statement_start_offset/2+1,
        (CASE WHEN qs.statement_end_offset = -1
              THEN LEN(CONVERT(nvarchar(max), qt.text)) * 2
              ELSE qs.statement_end_offset
         END - qs.statement_start_offset)/2) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) as qt
ORDER BY qs.total_logical_reads DESC;
```

[Back to top](#table-of-contents)

---

## 📊 SQL Server Index Types

### 1. Clustered Index
```sql
-- Clustered index (one per table)
CREATE CLUSTERED INDEX IX_Orders_OrderDate 
ON Orders (OrderDate ASC);

-- Best practices:
-- - Choose narrow, unique, and sequential keys
-- - Avoid frequent updates to clustered index key
-- - Use for range queries
```

### 2. Non-Clustered Index
```sql
-- Non-clustered index with included columns
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID_Includes
ON Orders (CustomerID)
INCLUDE (OrderDate, TotalAmount, Status);

-- Best practices:
-- - Up to 999 per table
-- - Use INCLUDE for non-key columns
-- - Consider index key order
```

### 3. Columnstore Index
```sql
-- Clustered columnstore index for analytics
CREATE CLUSTERED COLUMNSTORE INDEX CCIX_SalesHistory
ON SalesHistory;

-- Non-clustered columnstore for mixed workloads
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCIX_Orders_Analytics
ON Orders (CustomerID, OrderDate, TotalAmount, ProductID)
WHERE OrderDate >= '2023-01-01';

-- Best practices:
-- - Excellent for analytics and reporting
-- - Batch mode execution
-- - High compression ratios
```

### 4. Filtered Index
```sql
-- Filtered index for specific conditions
CREATE NONCLUSTERED INDEX IX_Orders_ActiveCustomers_Filtered
ON Orders (CustomerID, OrderDate)
WHERE Status = 'Active' AND OrderDate >= '2024-01-01';

-- Best practices:
-- - Reduces index size and maintenance
-- - Improves query performance for specific filters
-- - Lower storage and update costs
```

### 5. Unique Index
```sql
-- Unique index to enforce uniqueness
CREATE UNIQUE NONCLUSTERED INDEX IX_Customers_Email_Unique
ON Customers (Email);

-- Composite unique index
CREATE UNIQUE NONCLUSTERED INDEX IX_OrderDetails_OrderProduct_Unique
ON OrderDetails (OrderID, ProductID);

-- Best practices:
-- - Automatically created with PRIMARY KEY and UNIQUE constraints
-- - Prevents duplicate values
-- - Can be used for foreign key relationships
```

### 6. Spatial Index
```sql
-- Spatial index for geographic data
CREATE SPATIAL INDEX IX_Locations_Geography_Spatial
ON Locations (LocationPoint)
USING GEOGRAPHY_GRID
WITH (
    GRIDS = (LEVEL_1 = MEDIUM, LEVEL_2 = MEDIUM, LEVEL_3 = MEDIUM, LEVEL_4 = MEDIUM),
    CELLS_PER_OBJECT = 16
);

-- Best practices:
-- - Essential for geographic queries
-- - Multiple tessellation options
-- - Consider data density for grid configuration
```

### 7. Full-Text Index
```sql
-- Full-text catalog and index
CREATE FULLTEXT CATALOG ProductCatalog;

CREATE FULLTEXT INDEX ON Products (ProductName, Description)
KEY INDEX PK_Products
ON ProductCatalog;

-- Full-text search query
SELECT ProductID, ProductName, Description
FROM Products
WHERE CONTAINS(ProductName, '"SQL Server" OR "Database"');

-- Best practices:
-- - Excellent for text search operations
-- - Supports linguistic searches
-- - Regular population schedule needed
```
[Back to top](#table-of-contents)

---

## ⚙️ Parameter Configuration

### Memory Configuration
```sql
-- Memory settings for production environment (64GB RAM server)
USE master;
GO

EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

-- Set maximum server memory (leave 8GB for OS on dedicated server)
EXEC sp_configure 'max server memory (MB)', 57344;  -- 56GB
EXEC sp_configure 'min server memory (MB)', 4096;   -- 4GB minimum

RECONFIGURE;
```

### Parallelism Configuration
```sql
-- Parallelism settings
EXEC sp_configure 'max degree of parallelism', 8;   -- Half of CPU cores
EXEC sp_configure 'cost threshold for parallelism', 50;  -- Higher threshold

RECONFIGURE;
```

### TempDB Configuration
```sql
-- TempDB optimization (multiple data files)
USE master;
GO

-- Create multiple TempDB data files (one per CPU core, up to 8)
ALTER DATABASE tempdb 
ADD FILE (
    NAME = 'tempdev2',
    FILENAME = 'C:\TempDB\tempdev2.ndf',
    SIZE = 1024MB,
    FILEGROWTH = 256MB
);

ALTER DATABASE tempdb 
ADD FILE (
    NAME = 'tempdev3',
    FILENAME = 'C:\TempDB\tempdev3.ndf',
    SIZE = 1024MB,
    FILEGROWTH = 256MB
);

-- Continue adding files as needed...

-- Optimize TempDB settings
EXEC sp_configure 'optimize for ad hoc workloads', 1;
RECONFIGURE;
```

### Auto-Configuration Script
```sql
-- Script to calculate settings based on hardware
DECLARE @TotalMemoryMB INT;
DECLARE @RecommendedMaxMemory INT;
DECLARE @CPUCount INT;
DECLARE @RecommendedMAXDOP INT;

-- Get system information
SELECT @TotalMemoryMB = physical_memory_kb / 1024 
FROM sys.dm_os_sys_info;

SELECT @CPUCount = cpu_count 
FROM sys.dm_os_sys_info;

-- Calculate recommended settings
SET @RecommendedMaxMemory = @TotalMemoryMB - 4096;  -- Leave 4GB for OS
SET @RecommendedMAXDOP = CASE 
    WHEN @CPUCount <= 8 THEN @CPUCount
    WHEN @CPUCount <= 16 THEN 8
    ELSE @CPUCount / 2
END;

-- Show recommendations
SELECT 
    'Total System Memory (MB)' AS config_name, 
    @TotalMemoryMB AS current_value,
    @TotalMemoryMB AS recommended_value
UNION ALL
SELECT 
    'Max Server Memory (MB)', 
    CAST(value AS INT),
    @RecommendedMaxMemory
FROM sys.configurations WHERE name = 'max server memory (MB)'
UNION ALL
SELECT 
    'Max Degree of Parallelism',
    CAST(value AS INT),
    @RecommendedMAXDOP
FROM sys.configurations WHERE name = 'max degree of parallelism';
```
[Back to top](#table-of-contents)

---

## 🖥️ On-Premise Tuning

### SQL Server Instance Configuration
```sql
-- Optimized instance configurations (64GB RAM, 16 cores)
USE master;
GO

-- Advanced configurations
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

-- Memory settings (leave 8GB for OS on dedicated server)
EXEC sp_configure 'max server memory (MB)', 57344;  -- 56GB
EXEC sp_configure 'min server memory (MB)', 4096;   -- 4GB minimum

-- Parallelism
EXEC sp_configure 'max degree of parallelism', 8;   -- Half of cores
EXEC sp_configure 'cost threshold for parallelism', 50;

-- General optimizations
EXEC sp_configure 'optimize for ad hoc workloads', 1;
EXEC sp_configure 'backup compression default', 1;
EXEC sp_configure 'fill factor (%)', 90;            -- 10% free space in indexes

-- Advanced settings
EXEC sp_configure 'max worker threads', 0;          -- Auto-configure
EXEC sp_configure 'network packet size (B)', 4096;
EXEC sp_configure 'remote query timeout (s)', 600;

RECONFIGURE;
```

### Database File Configuration
```sql
-- Database file optimization
USE master;
GO

-- Set initial sizes and growth settings for data files
ALTER DATABASE [YourDatabase] 
MODIFY FILE (
    NAME = 'YourDatabase',
    SIZE = 10GB,
    FILEGROWTH = 1GB
);

-- Set initial sizes and growth settings for log files
ALTER DATABASE [YourDatabase] 
MODIFY FILE (
    NAME = 'YourDatabase_Log',
    SIZE = 2GB,
    FILEGROWTH = 512MB
);

-- Add additional data files if needed (for large databases)
ALTER DATABASE [YourDatabase]
ADD FILE (
    NAME = 'YourDatabase_Data2',
    FILENAME = 'C:\Data\YourDatabase_Data2.ndf',
    SIZE = 10GB,
    FILEGROWTH = 1GB
);
```

### Maintenance Plans
```sql
-- Index maintenance script
USE [YourDatabase];
GO

DECLARE @fragmentation FLOAT;
DECLARE @objectid INT;
DECLARE @indexid INT;
DECLARE @schemaname NVARCHAR(130);
DECLARE @objectname NVARCHAR(130);
DECLARE @indexname NVARCHAR(130);

DECLARE index_cursor CURSOR FOR
SELECT 
    object_id,
    index_id,
    avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')
WHERE avg_fragmentation_in_percent > 10
AND index_id > 0;

OPEN index_cursor;

FETCH NEXT FROM index_cursor 
INTO @objectid, @indexid, @fragmentation;

WHILE @@FETCH_STATUS = 0
BEGIN
    SELECT 
        @schemaname = s.name,
        @objectname = o.name,
        @indexname = i.name
    FROM sys.objects o
    INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
    INNER JOIN sys.indexes i ON o.object_id = i.object_id
    WHERE o.object_id = @objectid AND i.index_id = @indexid;

    IF @fragmentation > 30
    BEGIN
        -- Rebuild index
        EXEC ('ALTER INDEX [' + @indexname + '] ON [' + @schemaname + '].[' + @objectname + '] REBUILD WITH (ONLINE = ON, MAXDOP = 1)');
        PRINT 'Rebuilt index ' + @indexname + ' on ' + @schemaname + '.' + @objectname;
    END
    ELSE IF @fragmentation > 10
    BEGIN
        -- Reorganize index
        EXEC ('ALTER INDEX [' + @indexname + '] ON [' + @schemaname + '].[' + @objectname + '] REORGANIZE');
        PRINT 'Reorganized index ' + @indexname + ' on ' + @schemaname + '.' + @objectname;
    END

    FETCH NEXT FROM index_cursor 
    INTO @objectid, @indexid, @fragmentation;
END

CLOSE index_cursor;
DEALLOCATE index_cursor;
```
[Back to top](#table-of-contents)

---

## ☁️ Cloud Tuning

### Azure SQL Database
```sql
-- Azure SQL Database specific optimizations

-- Enable automatic tuning
ALTER DATABASE [YourDatabase] 
SET AUTOMATIC_TUNING (FORCE_LAST_GOOD_PLAN = ON);

ALTER DATABASE [YourDatabase] 
SET AUTOMATIC_TUNING (CREATE_INDEX = ON);

ALTER DATABASE [YourDatabase] 
SET AUTOMATIC_TUNING (DROP_INDEX = ON);

-- Query Store configuration for Azure SQL
ALTER DATABASE [YourDatabase] 
SET QUERY_STORE = ON 
(
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 60,
    MAX_STORAGE_SIZE_MB = 1000,
    QUERY_CAPTURE_MODE = AUTO,
    SIZE_BASED_CLEANUP_MODE = AUTO
);

-- Check service tier and resource limits
SELECT 
    DATABASEPROPERTYEX(DB_NAME(), 'ServiceObjective') AS ServiceTier,
    DATABASEPROPERTYEX(DB_NAME(), 'Edition') AS Edition,
    DATABASEPROPERTYEX(DB_NAME(), 'MaxSizeInBytes') AS MaxSize;

-- Monitor DTU/eDTU usage
SELECT 
    end_time,
    avg_cpu_percent,
    avg_data_io_percent,
    avg_log_write_percent,
    avg_memory_usage_percent,
    xtp_storage_percent,
    max_worker_percent,
    max_session_percent
FROM sys.dm_db_resource_stats
ORDER BY end_time DESC;
```

### AWS RDS SQL Server
```sql
-- AWS RDS specific configurations

-- Enable Query Store
ALTER DATABASE [YourDatabase] 
SET QUERY_STORE = ON;

-- Check RDS specific settings
SELECT 
    name,
    value,
    value_in_use,
    description
FROM sys.configurations
WHERE name IN (
    'max server memory (MB)',
    'max degree of parallelism',
    'cost threshold for parallelism',
    'optimize for ad hoc workloads'
);

-- Monitor CloudWatch metrics equivalent
SELECT 
    counter_name,
    cntr_value,
    cntr_type
FROM sys.dm_os_performance_counters
WHERE counter_name IN (
    'Buffer cache hit ratio',
    'Page life expectancy',
    'Batch Requests/sec',
    'SQL Compilations/sec'
);
```

### Google Cloud SQL Server
```sql
-- Google Cloud SQL specific optimizations

-- Enable Query Insights equivalent through Query Store
ALTER DATABASE [YourDatabase] 
SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 60,
    MAX_STORAGE_SIZE_MB = 1000,
    QUERY_CAPTURE_MODE = AUTO
);

-- Check current configuration
SELECT 
    name,
    value_in_use,
    description
FROM sys.configurations
WHERE is_advanced = 1
ORDER BY name;

-- Monitor connection counts
SELECT 
    session_id,
    login_time,
    host_name,
    program_name,
    login_name,
    status,
    cpu_time,
    memory_usage,
    total_scheduled_time,
    reads,
    writes,
    logical_reads
FROM sys.dm_exec_sessions
WHERE is_user_process = 1;
```
[Back to top](#table-of-contents)

---

## 🔧 Specialized Tools

### Extended Events (Replacing SQL Profiler)
```sql
-- Create Extended Events session for performance monitoring
CREATE EVENT SESSION [Performance_Monitoring] ON SERVER 
ADD EVENT sqlserver.sql_batch_completed(
    ACTION(sqlserver.client_app_name,sqlserver.client_hostname,sqlserver.database_name,sqlserver.username)
    WHERE ([duration] > 1000000 AND [cpu_time] > 500000)),  -- > 1 second duration, > 0.5 second CPU
ADD EVENT sqlserver.rpc_completed(
    ACTION(sqlserver.client_app_name,sqlserver.client_hostname,sqlserver.database_name,sqlserver.username)
    WHERE ([duration] > 1000000 AND [cpu_time] > 500000)),
ADD EVENT sqlserver.blocked_process_report,
ADD EVENT sqlserver.deadlock_graph
ADD TARGET package0.event_file(SET filename=N'C:\ExtendedEvents\Performance_Monitoring')
WITH (MAX_MEMORY=4096 KB,EVENT_RETENTION_MODE=ALLOW_SINGLE_EVENT_LOSS,MAX_DISPATCH_LATENCY=30 SECONDS,MAX_EVENT_SIZE=0 KB,MEMORY_PARTITION_MODE=NONE,TRACK_CAUSALITY=OFF,STARTUP_STATE=ON);

-- Start the Extended Events session
ALTER EVENT SESSION [Performance_Monitoring] ON SERVER STATE = START;

-- Query Extended Events data
SELECT 
    CAST(event_data AS XML) as event_data_xml,
    CAST(event_data AS XML).value('(event/@name)[1]', 'VARCHAR(50)') AS event_name,
    CAST(event_data AS XML).value('(event/@timestamp)[1]', 'DATETIME2') AS event_time,
    CAST(event_data AS XML).value('(event/data[@name="duration"]/value)[1]', 'BIGINT') AS duration_microseconds,
    CAST(event_data AS XML).value('(event/data[@name="cpu_time"]/value)[1]', 'BIGINT') AS cpu_time_microseconds,
    CAST(event_data AS XML).value('(event/data[@name="logical_reads"]/value)[1]', 'BIGINT') AS logical_reads,
    CAST(event_data AS XML).value('(event/data[@name="statement"]/value)[1]', 'NVARCHAR(MAX)') AS sql_text
FROM sys.fn_xe_file_target_read_file('C:\ExtendedEvents\Performance_Monitoring*.xel', NULL, NULL, NULL);
```

### Query Store Analysis
```sql
-- Enable Query Store
ALTER DATABASE [YourDatabase] 
SET QUERY_STORE = ON 
(
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    INTERVAL_LENGTH_MINUTES = 60,
    MAX_STORAGE_SIZE_MB = 1000,
    QUERY_CAPTURE_MODE = AUTO,
    SIZE_BASED_CLEANUP_MODE = AUTO,
    MAX_PLANS_PER_QUERY = 200
);

-- Query Store - Top resource consuming queries
SELECT TOP 20
    qsq.query_id,
    qst.query_sql_text,
    qrs.count_executions,
    qrs.avg_duration / 1000.0 AS avg_duration_ms,
    qrs.avg_cpu_time / 1000.0 AS avg_cpu_time_ms,
    qrs.avg_logical_io_reads,
    qrs.avg_physical_io_reads,
    qrs.avg_query_max_used_memory,
    qrs.last_execution_time
FROM sys.query_store_query_text qst
INNER JOIN sys.query_store_query qsq ON qst.query_text_id = qsq.query_text_id
INNER JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
INNER JOIN sys.query_store_runtime_stats qrs ON qsp.plan_id = qrs.plan_id
WHERE qrs.last_execution_time > DATEADD(hour, -24, GETUTCDATE())
ORDER BY qrs.avg_cpu_time DESC;

-- Query Store - Regressed queries
SELECT 
    qsq.query_id,
    qst.query_sql_text,
    qsp.plan_id,
    qrs.avg_duration / 1000.0 AS current_avg_duration_ms,
    qrs.avg_cpu_time / 1000.0 AS current_avg_cpu_time_ms,
    qrs.count_executions AS current_execution_count,
    qrs.last_execution_time
FROM sys.query_store_query_text qst
INNER JOIN sys.query_store_query qsq ON qst.query_text_id = qsq.query_text_id
INNER JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
INNER JOIN sys.query_store_runtime_stats qrs ON qsp.plan_id = qrs.plan_id
WHERE qrs.last_execution_time > DATEADD(hour, -1, GETUTCDATE())
    AND qrs.avg_duration > (
        SELECT AVG(avg_duration) * 2
        FROM sys.query_store_runtime_stats qrs2
        INNER JOIN sys.query_store_plan qsp2 ON qrs2.plan_id = qsp2.plan_id
        WHERE qsp2.query_id = qsq.query_id
            AND qrs2.last_execution_time BETWEEN 
                DATEADD(hour, -25, GETUTCDATE()) AND DATEADD(hour, -1, GETUTCDATE())
    )
ORDER BY qrs.avg_duration DESC;
```

### Resource Governor Configuration
```sql
-- Create resource pools
CREATE RESOURCE POOL ReportingPool
WITH (
    MIN_CPU_PERCENT = 0,
    MAX_CPU_PERCENT = 30,
    MIN_MEMORY_PERCENT = 0,
    MAX_MEMORY_PERCENT = 25
);

CREATE RESOURCE POOL OLTPPool
WITH (
    MIN_CPU_PERCENT = 50,
    MAX_CPU_PERCENT = 100,
    MIN_MEMORY_PERCENT = 50,
    MAX_MEMORY_PERCENT = 100
);

-- Create workload groups
CREATE WORKLOAD GROUP ReportingGroup
WITH (
    GROUP_MAX_REQUESTS = 10,
    IMPORTANCE = LOW,
    REQUEST_MAX_CPU_TIME_SEC = 300,
    REQUEST_MAX_MEMORY_GRANT_PERCENT = 10,
    REQUEST_MEMORY_GRANT_TIMEOUT_SEC = 120,
    MAX_DOP = 2
) USING ReportingPool;

CREATE WORKLOAD GROUP OLTPGroup
WITH (
    GROUP_MAX_REQUESTS = 0,  -- Unlimited
    IMPORTANCE = HIGH,
    REQUEST_MAX_CPU_TIME_SEC = 0,  -- Unlimited
    REQUEST_MAX_MEMORY_GRANT_PERCENT = 25,
    REQUEST_MEMORY_GRANT_TIMEOUT_SEC = 0,
    MAX_DOP = 8
) USING OLTPPool;

-- Create classifier function
CREATE FUNCTION dbo.ResourceGovernorClassifier()
RETURNS SYSNAME
WITH SCHEMABINDING
AS
BEGIN
    DECLARE @WorkloadGroup SYSNAME;
    
    IF (SUSER_NAME() = 'ReportingUser' OR APP_NAME() LIKE '%SSRS%' OR APP_NAME() LIKE '%Report%')
        SET @WorkloadGroup = 'ReportingGroup';
    ELSE
        SET @WorkloadGroup = 'OLTPGroup';
    
    RETURN @WorkloadGroup;
END;

-- Apply Resource Governor configuration
ALTER RESOURCE GOVERNOR WITH (CLASSIFIER_FUNCTION = dbo.ResourceGovernorClassifier);
ALTER RESOURCE GOVERNOR RECONFIGURE;
```

### Always On Availability Groups
```sql
-- Create Availability Group (on primary replica)
CREATE AVAILABILITY GROUP [AG_ProductionDB]
WITH (
    AUTOMATED_BACKUP_PREFERENCE = SECONDARY,
    FAILURE_CONDITION_LEVEL = 3,
    HEALTH_CHECK_TIMEOUT = 30000
)
FOR DATABASE [ProductionDB]
REPLICA ON 
    'SQL-PRIMARY' WITH (
        ENDPOINT_URL = 'TCP://sql-primary.domain.com:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 30,
        SECONDARY_ROLE(ALLOW_CONNECTIONS = NO)
    ),
    'SQL-SECONDARY' WITH (
        ENDPOINT_URL = 'TCP://sql-secondary.domain.com:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 50,
        SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY)
    ),
    'SQL-READONLY' WITH (
        ENDPOINT_URL = 'TCP://sql-readonly.domain.com:5022',
        AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT,
        FAILOVER_MODE = MANUAL,
        BACKUP_PRIORITY = 100,
        SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY)
    );

-- Monitor Availability Group health
SELECT 
    ag.name AS availability_group_name,
    replica_server_name,
    role_desc,
    operational_state_desc,
    connected_state_desc,
    synchronization_health_desc,
    synchronization_state_desc
FROM sys.availability_replicas ar
LEFT JOIN sys.dm_hadr_availability_replica_states ars ON ar.replica_id = ars.replica_id
LEFT JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
ORDER BY ag.name, role_desc DESC;
```

[Back to top](#table-of-contents)

---

## 💼 Practical Cases

### Case 1: E-commerce Database Optimization
**Problem**: Online store with 50M+ products experiencing slow search and checkout processes.

**Solution Implemented**:
```sql
-- Created columnstore index for analytics
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCIX_Orders_Analytics
ON Orders (CustomerID, OrderDate, TotalAmount, ProductCategory, PaymentMethod)
WHERE OrderDate >= '2023-01-01';

-- Optimized product search index
CREATE NONCLUSTERED INDEX IX_Products_Search_Optimized
ON Products (CategoryID, BrandID, IsActive)
INCLUDE (ProductName, Price, Description, ImageURL)
WHERE IsActive = 1;

-- Partitioned large tables by date
CREATE PARTITION FUNCTION OrderDatePartitionFunction (DATE)
AS RANGE RIGHT FOR VALUES 
('2023-01-01', '2023-04-01', '2023-07-01', '2023-10-01', '2024-01-01');

CREATE PARTITION SCHEME OrderDatePartitionScheme
AS PARTITION OrderDatePartitionFunction
TO ([PRIMARY], [Q1_2023], [Q2_2023], [Q3_2023], [Q4_2023], [Q1_2024]);

-- Applied table partitioning
CREATE TABLE Orders_New (
    OrderID BIGINT IDENTITY(1,1),
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    TotalAmount DECIMAL(10,2),
    Status VARCHAR(20),
    INDEX IX_Orders_Partitioned CLUSTERED (OrderDate, OrderID)
) ON OrderDatePartitionScheme(OrderDate);
```

**Results**:
- **Search response time**: Reduced from 3.2s to 180ms (94% improvement)
- **Checkout process**: Improved from 8s to 1.1s (86% improvement)
- **Analytics queries**: 15x faster execution
- **Storage savings**: 40% reduction through columnstore compression

### Case 2: Financial Services Data Warehouse
**Problem**: Investment firm processing 500GB+ of daily trading data with complex reporting requirements.

**Solution Implemented**:
```sql
-- Implemented clustered columnstore with archival compression
CREATE CLUSTERED COLUMNSTORE INDEX CCIX_TradingData_Archive
ON TradingDataHistorical
WITH (DATA_COMPRESSION = COLUMNSTORE_ARCHIVE);

-- Created aggregate tables with indexed views
CREATE VIEW dbo.DailyTradingSummary
WITH SCHEMABINDING
AS
SELECT 
    TradingDate,
    SecurityID,
    COUNT_BIG(*) AS TradeCount,
    SUM(Volume) AS TotalVolume,
    SUM(TradeValue) AS TotalValue,
    AVG(Price) AS AvgPrice
FROM dbo.TradingData
GROUP BY TradingDate, SecurityID;

CREATE UNIQUE CLUSTERED INDEX IX_DailyTradingSummary
ON dbo.DailyTradingSummary (TradingDate, SecurityID);

-- Implemented Resource Governor for workload separation
CREATE WORKLOAD GROUP AnalyticsGroup
WITH (
    IMPORTANCE = MEDIUM,
    REQUEST_MAX_MEMORY_GRANT_PERCENT = 50,
    MAX_DOP = 4
) USING AnalyticsPool;
```

**Results**:
- **Data compression**: 85% storage reduction
- **Report generation**: From 45 minutes to 3 minutes
- **Concurrent user capacity**: Increased from 50 to 200 users
- **Resource isolation**: Analytics workloads no longer impact OLTP

### Case 3: Healthcare System Integration
**Problem**: Hospital management system with 24/7 availability requirements and strict compliance needs.

**Solution Implemented**:
```sql
-- Implemented Always On with multiple secondaries
-- (Previous Always On configuration code applies here)

-- Row Level Security for patient data
CREATE SCHEMA Security;
GO

CREATE FUNCTION Security.PatientAccessPredicate(@PatientID INT)
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS AccessResult
WHERE @PatientID IN (
    SELECT PatientID FROM dbo.UserPatientAccess 
    WHERE UserID = USER_ID()
) OR IS_MEMBER('db_datareader') = 1;

ALTER TABLE dbo.PatientRecords
ADD FILTER PREDICATE Security.PatientAccessPredicate(PatientID),
BLOCK PREDICATE Security.PatientAccessPredicate(PatientID) ON AFTER INSERT;

ALTER TABLE dbo.PatientRecords ENABLE ROW LEVEL SECURITY;

-- Temporal tables for audit compliance
ALTER TABLE dbo.PatientRecords
ADD 
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo);

ALTER TABLE dbo.PatientRecords
SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.PatientRecords_History));

-- Transparent Data Encryption
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongPassword123!';

CREATE CERTIFICATE TDECert WITH SUBJECT = 'TDE Certificate';

CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE TDECert;

ALTER DATABASE [HospitalDB] SET ENCRYPTION ON;
```

**Results**:
- **High Availability**: 99.99% uptime achieved
- **Compliance**: Full audit trail and data encryption
- **Performance**: Sub-second response for critical patient lookups
- **Security**: Row-level access control implemented

[Back to top](#table-of-contents)

---

## 📊 Automated Monitoring

### PowerShell Monitoring Script
```powershell
# SQL Server Health Check Automation
param(
    [string]$ServerInstance = "localhost",
    [string]$Database = "master",
    [string]$EmailRecipient = "dba@company.com"
)

# Import SQL Server module
Import-Module SqlServer

# Define thresholds
$CPUThreshold = 80
$MemoryThreshold = 90
$DiskSpaceThreshold = 10
$BufferCacheThreshold = 95
$PageLifeExpectancyThreshold = 300

# Function to send alert email
function Send-Alert {
    param([string]$Subject, [string]$Body)
    
    $EmailParams = @{
        To = $EmailRecipient
        From = "sql-monitor@company.com"
        Subject = $Subject
        Body = $Body
        SmtpServer = "smtp.company.com"
        Port = 587
        UseSsl = $true
    }
    Send-MailMessage @EmailParams
}

# Check CPU Usage
$CPUQuery = @"
SELECT TOP 1 
    AVG(signal_wait_time_ms) * 100.0 / AVG(wait_time_ms) AS cpu_utilization
FROM sys.dm_os_wait_stats
WHERE wait_time_ms > 0
"@

$CPUUsage = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $Database -Query $CPUQuery
if ($CPUUsage.cpu_utilization -gt $CPUThreshold) {
    Send-Alert "HIGH CPU ALERT" "CPU usage is $($CPUUsage.cpu_utilization)% on $ServerInstance"
}

# Check Memory Usage
$MemoryQuery = @"
SELECT 
    (committed_kb * 100.0) / committed_target_kb AS memory_utilization
FROM sys.dm_os_sys_info
"@

$MemoryUsage = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $Database -Query $MemoryQuery
if ($MemoryUsage.memory_utilization -gt $MemoryThreshold) {
    Send-Alert "HIGH MEMORY ALERT" "Memory usage is $($MemoryUsage.memory_utilization)% on $ServerInstance"
}

# Check Buffer Cache Hit Ratio
$BufferCacheQuery = @"
SELECT 
    (cntr_value * 100.0 / 
        (SELECT cntr_value FROM sys.dm_os_performance_counters 
         WHERE counter_name = 'Buffer cache hit ratio base')) AS buffer_cache_hit_ratio
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Buffer cache hit ratio'
AND object_name LIKE '%Buffer Manager%'
"@

$BufferCache = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $Database -Query $BufferCacheQuery
if ($BufferCache.buffer_cache_hit_ratio -lt $BufferCacheThreshold) {
    Send-Alert "LOW BUFFER CACHE HIT RATIO" "Buffer cache hit ratio is $($BufferCache.buffer_cache_hit_ratio)% on $ServerInstance"
}

# Check Page Life Expectancy
$PLEQuery = @"
SELECT cntr_value AS page_life_expectancy
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Page life expectancy'
AND object_name LIKE '%Buffer Manager%'
"@

$PLE = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $Database -Query $PLEQuery
if ($PLE.page_life_expectancy -lt $PageLifeExpectancyThreshold) {
    Send-Alert "LOW PAGE LIFE EXPECTANCY" "Page Life Expectancy is $($PLE.page_life_expectancy) seconds on $ServerInstance"
}

# Check Disk Space
$DiskSpaceQuery = @"
EXEC xp_fixeddrives
"@

$DiskSpace = Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $Database -Query $DiskSpaceQuery
foreach ($Drive in $DiskSpace) {
    if ($Drive.MB_Free -lt ($DiskSpaceThreshold * 1024)) {  # Convert GB to MB
        Send-Alert "LOW DISK SPACE ALERT" "Drive $($Drive.Drive) has only $($Drive.MB_Free) MB free on $ServerInstance"
    }
}

Write-Host "Health check completed for $ServerInstance" -ForegroundColor Green
```

### C# Monitoring Application
```csharp
using System;
using System.Data.SqlClient;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System.Net.Mail;

public class SqlServerMonitor
{
    private readonly string _connectionString;
    private readonly ILogger<SqlServerMonitor> _logger;
    private readonly SmtpClient _smtpClient;
    
    public SqlServerMonitor(IConfiguration config, ILogger<SqlServerMonitor> logger)
    {
        _connectionString = config.GetConnectionString("SqlServer");
        _logger = logger;
        _smtpClient = new SmtpClient(config["Email:SmtpServer"])
        {
            Port = int.Parse(config["Email:Port"]),
            EnableSsl = true,
            Credentials = new System.Net.NetworkCredential(
                config["Email:Username"], 
                config["Email:Password"])
        };
    }
    
    public async Task<PerformanceMetrics> GetPerformanceMetricsAsync()
    {
        using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        
        var metrics = new PerformanceMetrics();
        
        // Get Buffer Cache Hit Ratio
        var bufferCacheQuery = @"
            SELECT 
                (cntr_value * 100.0 / 
                    (SELECT cntr_value FROM sys.dm_os_performance_counters 
                     WHERE counter_name = 'Buffer cache hit ratio base')) AS hit_ratio
            FROM sys.dm_os_performance_counters 
            WHERE counter_name = 'Buffer cache hit ratio'
            AND object_name LIKE '%Buffer Manager%'";
            
        using var bufferCmd = new SqlCommand(bufferCacheQuery, connection);
        metrics.BufferCacheHitRatio = (decimal)await bufferCmd.ExecuteScalarAsync();
        
        // Get Page Life Expectancy
        var pleQuery = @"
            SELECT cntr_value 
            FROM sys.dm_os_performance_counters 
            WHERE counter_name = 'Page life expectancy'
            AND object_name LIKE '%Buffer Manager%'";
            
        using var pleCmd = new SqlCommand(pleQuery, connection);
        metrics.PageLifeExpectancy = (long)await pleCmd.ExecuteScalarAsync();
        
        // Get Batch Requests per Second
        var batchQuery = @"
            SELECT cntr_value 
            FROM sys.dm_os_performance_counters 
            WHERE counter_name = 'Batch Requests/sec'";
            
        using var batchCmd = new SqlCommand(batchQuery, connection);
        metrics.BatchRequestsPerSecond = (long)await batchCmd.ExecuteScalarAsync();
        
        // Get Wait Statistics
        var waitQuery = @"
            SELECT TOP 5
                wait_type,
                wait_time_ms,
                waiting_tasks_count,
                (wait_time_ms - signal_wait_time_ms) AS resource_wait_ms,
                signal_wait_time_ms,
                100.0 * wait_time_ms / SUM(wait_time_ms) OVER() AS percentage
            FROM sys.dm_os_wait_stats
            WHERE wait_type NOT IN ('SLEEP_TASK', 'BROKER_TO_FLUSH', 'SQLTRACE_INCREMENTAL_FLUSH_SLEEP')
            AND wait_time_ms > 0
            ORDER BY wait_time_ms DESC";
            
        using var waitCmd = new SqlCommand(waitQuery, connection);
        using var waitReader = await waitCmd.ExecuteReaderAsync();
        
        while (await waitReader.ReadAsync())
        {
            metrics.TopWaits.Add(new WaitStat
            {
                WaitType = waitReader.GetString("wait_type"),
                WaitTimeMs = waitReader.GetInt64("wait_time_ms"),
                WaitingTasksCount = waitReader.GetInt64("waiting_tasks_count"),
                ResourceWaitMs = waitReader.GetInt64("resource_wait_ms"),
                SignalWaitMs = waitReader.GetInt64("signal_wait_time_ms"),
                Percentage = waitReader.GetDecimal("percentage")
            });
        }
        
        return metrics;
    }
    
    public async Task CheckAlertsAsync()
    {
        var metrics = await GetPerformanceMetricsAsync();
        
        // Check Buffer Cache Hit Ratio
        if (metrics.BufferCacheHitRatio < 95)
        {
            await SendAlertAsync("Low Buffer Cache Hit Ratio", 
                $"Buffer cache hit ratio is {metrics.BufferCacheHitRatio:F2}%");
        }
        
        // Check Page Life Expectancy
        if (metrics.PageLifeExpectancy < 300)
        {
            await SendAlertAsync("Low Page Life Expectancy", 
                $"Page Life Expectancy is {metrics.PageLifeExpectancy} seconds");
        }
        
        // Check for problematic waits
        foreach (var wait in metrics.TopWaits)
        {
            if (wait.WaitType.Contains("PAGEIOLATCH") && wait.Percentage > 20)
            {
                await SendAlertAsync("High I/O Waits Detected", 
                    $"{wait.WaitType} represents {wait.Percentage:F2}% of total waits");
            }
        }
    }
    
    private async Task SendAlertAsync(string subject, string body)
    {
        var message = new MailMessage
        {
            From = new MailAddress("sql-monitor@company.com"),
            Subject = $"SQL Server Alert: {subject}",
            Body = $"{body}\n\nTimestamp: {DateTime.Now:yyyy-MM-dd HH:mm:ss}",
            IsBodyHtml = false
        };
        
        message.To.Add("dba@company.com");
        
        try
        {
            await _smtpClient.SendMailAsync(message);
            _logger.LogInformation($"Alert sent: {subject}");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Failed to send alert: {subject}");
        }
    }
}

public class PerformanceMetrics
{
    public decimal BufferCacheHitRatio { get; set; }
    public long PageLifeExpectancy { get; set; }
    public long BatchRequestsPerSecond { get; set; }
    public List<WaitStat> TopWaits { get; set; } = new List<WaitStat>();
}

public class WaitStat
{
    public string WaitType { get; set; }
    public long WaitTimeMs { get; set; }
    public long WaitingTasksCount { get; set; }
    public long ResourceWaitMs { get; set; }
    public long SignalWaitMs { get; set; }
    public decimal Percentage { get; set; }
}
```

### SQL Server Agent Jobs for Maintenance
```sql
-- Create maintenance job for index optimization
USE msdb;
GO

EXEC dbo.sp_add_job
    @job_name = N'Database Maintenance - Index Optimization';

EXEC dbo.sp_add_jobstep
    @job_name = N'Database Maintenance - Index Optimization',
    @step_name = N'Rebuild and Reorganize Indexes',
    @subsystem = N'TSQL',
    @command = N'
        DECLARE @sql NVARCHAR(MAX);
        DECLARE @dbname SYSNAME;
        
        DECLARE db_cursor CURSOR FOR
        SELECT name FROM sys.databases 
        WHERE state = 0 AND name NOT IN (''master'', ''model'', ''msdb'', ''tempdb'');
        
        OPEN db_cursor;
        FETCH NEXT FROM db_cursor INTO @dbname;
        
        WHILE @@FETCH_STATUS = 0
        BEGIN
            SET @sql = ''USE ['' + @dbname + ''];
            
            -- Rebuild indexes with > 30% fragmentation
            DECLARE @fragmentation FLOAT;
            DECLARE @objectid INT;
            DECLARE @indexid INT;
            DECLARE @schemaname NVARCHAR(130);
            DECLARE @objectname NVARCHAR(130);
            DECLARE @indexname NVARCHAR(130);
            
            DECLARE index_cursor CURSOR FOR
            SELECT object_id, index_id, avg_fragmentation_in_percent
            FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, ''''LIMITED'''')
            WHERE avg_fragmentation_in_percent > 10 AND index_id > 0;
            
            OPEN index_cursor;
            FETCH NEXT FROM index_cursor INTO @objectid, @indexid, @fragmentation;
            
            WHILE @@FETCH_STATUS = 0
            BEGIN
                SELECT @schemaname = s.name, @objectname = o.name, @indexname = i.name
                FROM sys.objects o
                INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
                INNER JOIN sys.indexes i ON o.object_id = i.object_id
                WHERE o.object_id = @objectid AND i.index_id = @indexid;
                
                IF @fragmentation > 30
                    EXEC (''''ALTER INDEX ['''''' + @indexname + ''''''] ON ['''''' + @schemaname + ''''].['''''' + @objectname + ''''] REBUILD WITH (ONLINE = ON, MAXDOP = 1)'''');
                ELSE IF @fragmentation > 10
                    EXEC (''''ALTER INDEX ['''''' + @indexname + ''''''] ON ['''''' + @schemaname + ''''].['''''' + @objectname + ''''] REORGANIZE'''');
                
                FETCH NEXT FROM index_cursor INTO @objectid, @indexid, @fragmentation;
            END
            
            CLOSE index_cursor;
            DEALLOCATE index_cursor;'';
            
            EXEC sp_executesql @sql;
            
            FETCH NEXT FROM db_cursor INTO @dbname;
        END
        
        CLOSE db_cursor;
        DEALLOCATE db_cursor;',
    @retry_attempts = 3,
    @retry_interval = 5;

-- Schedule the job to run every Sunday at 2 AM
EXEC dbo.sp_add_schedule
    @schedule_name = N'Weekly Sunday 2AM',
    @freq_type = 8,
    @freq_interval = 1,
    @freq_recurrence_factor = 1,
    @active_start_time = 20000;

EXEC dbo.sp_attach_schedule
    @job_name = N'Database Maintenance - Index Optimization',
    @schedule_name = N'Weekly Sunday 2AM';

EXEC dbo.sp_add_jobserver
    @job_name = N'Database Maintenance - Index Optimization';

-- Create statistics update job
EXEC dbo.sp_add_job
    @job_name = N'Database Maintenance - Update Statistics';

EXEC dbo.sp_add_jobstep
    @job_name = N'Database Maintenance - Update Statistics',
    @step_name = N'Update All Statistics',
    @subsystem = N'TSQL',
    @command = N'
        EXEC sp_MSforeachdb ''
        IF ''''?'''' NOT IN (''''master'''', ''''model'''', ''''msdb'''', ''''tempdb'''')
        BEGIN
            USE [?];
            EXEC sp_updatestats;
        END''';

-- Schedule statistics update daily at 6 AM
EXEC dbo.sp_add_schedule
    @schedule_name = N'Daily 6AM',
    @freq_type = 4,
    @freq_interval = 1,
    @active_start_time = 60000;

EXEC dbo.sp_attach_schedule
    @job_name = N'Database Maintenance - Update Statistics',
    @schedule_name = N'Daily 6AM';

EXEC dbo.sp_add_jobserver
    @job_name = N'Database Maintenance - Update Statistics';
```

[Back to top](#table-of-contents)

---
## 🛠️ Management Tools

| **Tool** | **Purpose** | **Platform** | **Free/Paid** |
|----------|-------------|--------------|---------------|
| **SQL Server Management Studio (SSMS)** | Primary Management Interface | Windows | Free |
| **Azure Data Studio** | Cross-platform SQL Editor | Windows/Mac/Linux | Free |
| **SQL Server Profiler** | Legacy Performance Monitoring | Windows | Free |
| **Extended Events** | Modern Performance Monitoring | All | Free |
| **Query Store** | Query Performance History | All | Free |
| **SQL Server Data Tools (SSDT)** | Database Development | Windows | Free |
| **sqlcmd** | Command Line Interface | All | Free |
| **PowerShell SqlServer Module** | Automation and Scripting | All | Free |
| **SQL Server Configuration Manager** | Service Configuration | Windows | Free |
| **Performance Monitor (PerfMon)** | System Performance Monitoring | Windows | Free |
| **Resource Monitor** | Real-time Resource Usage | Windows | Free |
| **SQL Sentry** | Advanced Monitoring Platform | All | Paid |
| **Redgate SQL Monitor** | Performance Monitoring | All | Paid |
| **SolarWinds Database Performance Analyzer** | Database Performance | All | Paid |
| **Quest Spotlight** | Real-time Monitoring | All | Paid |
| **ApexSQL Monitor** | Performance Monitoring | Windows | Paid |
| **IDERA SQL Diagnostic Manager** | Comprehensive Monitoring | All | Paid |
| **Paessler PRTG** | Infrastructure Monitoring | All | Paid |
| **DataDog** | Cloud Monitoring | All | Paid |
| **New Relic** | Application Performance Monitoring | All | Paid |
| **Azure Monitor** | Cloud Native Monitoring | Azure | Paid |
| **AWS CloudWatch** | AWS Native Monitoring | AWS | Paid |
| **Google Cloud Monitoring** | GCP Native Monitoring | GCP | Paid |
| **Grafana + Prometheus** | Open Source Monitoring | All | Free |
| **Zabbix** | Open Source Monitoring | All | Free |
| **Nagios** | Infrastructure Monitoring | All | Free/Paid |
| **PRTG Network Monitor** | Network and Database Monitoring | All | Paid |
| **ManageEngine Applications Manager** | Application Performance | All | Paid |
| **BMC TrueSight** | Enterprise Monitoring | All | Paid |
| **Dynatrace** | AI-Powered Monitoring | All | Paid |
| **AppDynamics** | Application Performance | All | Paid |
| **Datadog Database Monitoring** | Database Performance | All | Paid |
| **Azure Database Migration Service** | Cloud Migration | Azure | Free |
| **AWS Database Migration Service** | Cloud Migration | AWS | Paid |
| **Google Database Migration Service** | Cloud Migration | GCP | Paid |

---
[Back to top](#table-of-contents)

---

**[🏠 Back to Main Portfolio](../README.md#top)**

---

## Author & Maintainer
<table>
  <tr>
    <td width="96" valign="top">
      <img src="https://github.com/vandersantanna.png?size=160" alt="Vanderley Sant Anna" width="96" height="96">
    </td>
    <td valign="top">
      <strong>Vanderley Sant Anna</strong><br>
      Senior Database Engineer (DBE) / Senior Database Reliability Engineer (DBRE) / Senior DBA / DataOps Engineer
    </td>
  </tr>
</table>

**Preferred name:** Vander  

**Education:**  
- B.Sc. in Software Engineering — Centro Universitário de Maringá (UniCesumar) — *UniCesumar University Center*, Maringá, Brazil (2020)  
- Postgraduate Specialization (Lato Sensu) in Software Project Engineering — Universidade do Sul de Santa Catarina (UNISUL) — *Southern Santa Catarina University*, Florianópolis, Brazil (2008)  
- Technologist in Data Processing (*Tecnólogo em Processamento de Dados*) — Universidade do Estado de Santa Catarina (UDESC) — *Santa Catarina State University*, Joinville, Brazil (1995)  

**Certifications:**  
- Oracle OCP  
- MongoDB University — M102: MongoDB for DBAs  
- IBM Certified Database Associate — DB2 9 Fundamentals  

**Location & Timezone:** Blumenau, SC, Brazil (UTC−3) • **Availability:** Remote (Americas & Europe)

**Last Updated:** 2025-10-24 • **Status:** Actively maintained

## 📫 Contact
- **Email (primary):** [vandersantanna@gmail.com](mailto:vandersantanna@gmail.com)  
- **LinkedIn:** [linkedin.com/in/vandersantanna](https://www.linkedin.com/in/vandersantanna)  
- **GitHub:** [github.com/vandersantanna](https://github.com/vandersantanna)

<details>
  <summary><strong>Trademarks</strong></summary>

  <small>All product names, logos, and brands are property of their respective owners. 
  Use of these names is for identification purposes only and does not imply endorsement or affiliation.</small>
</details>


