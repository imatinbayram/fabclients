DECLARE @CurrentMonth INT = MONTH(GETDATE());
DECLARE @cols NVARCHAR(MAX);
DECLARE @sql NVARCHAR(MAX);

-- 2026 dynamic months
SELECT @cols =
    STRING_AGG(
        'ISNULL(SUM(CASE WHEN a.IL = 2026 AND a.AY = ' 
        + CAST(number AS VARCHAR) + 
        ' THEN a.MEBLEG END),0) AS [2026_' 
        + RIGHT('0' + CAST(number AS VARCHAR),2) + ']'
    , ', ')
FROM master..spt_values
WHERE type = 'P'
  AND number BETWEEN 1 AND @CurrentMonth;

SET @sql = '
WITH Categories AS (
    SELECT
        MikroID,
        CASE
            WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)),1,1) = ''1'' THEN ''Boru''
            WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)),1,1) = ''2'' THEN ''Boya''
            WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)),1,1) = ''3'' THEN ''Elektrik''
            WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)),1,1) = ''4'' THEN ''Toz''
            WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)),1,1) = ''5'' THEN ''Xirdavat''
            ELSE ''-''
        END AS Qol,
        Name AS Kateqoriya
    FROM BazarlamaHesabatDB.dbo.ProductGroup
    WHERE MikroID NOT IN (0, 999, 521, 601)
),

Sales AS (
    SELECT
        IL,
        AY,
        KATEQORIYA,
        MEBLEG
    FROM [MikroDB_V16_05].[dbo].[BazarlamaSatishCariStok_MB_Cari]
        (@tarix1, @tarix2, @anacari)
),

Agg AS (
    SELECT
        KATEQORIYA,
        IL,
        AY,
        SUM(MEBLEG) AS MEBLEG
    FROM Sales
    GROUP BY KATEQORIYA, IL, AY
)

SELECT
    c.MikroID,
    c.Qol,
    c.Kateqoriya,

    -- yearly totals
    ISNULL(SUM(CASE WHEN a.IL = 2025 THEN a.MEBLEG END),0) AS [2025_CEM],
    ISNULL(SUM(CASE WHEN a.IL = 2026 THEN a.MEBLEG END),0) AS [2026_CEM],

    -- monthly 2026 (dynamic)
    ' + @cols + '

FROM Categories c
LEFT JOIN Agg a
    ON c.Kateqoriya = a.KATEQORIYA

GROUP BY
    c.MikroID,
    c.Qol,
    c.Kateqoriya

ORDER BY
    c.MikroID;
';

EXEC sp_executesql 
    @sql,
    N'@tarix1 DATE, @tarix2 DATE, @anacari NVARCHAR(50)',
    @tarix1 = @tarix1,
    @tarix2 = @tarix2,
    @anacari = @anacari;