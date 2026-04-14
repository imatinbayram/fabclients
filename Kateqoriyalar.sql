SELECT
MikroID,
    CASE
        WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)), 1, 1) = '1' THEN 'Boru'
        WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)), 1, 1) = '2' THEN 'Boya'
        WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)), 1, 1) = '3' THEN 'Elektrik'
        WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)), 1, 1) = '4' THEN 'Toz'
        WHEN SUBSTRING(CAST(MikroID AS VARCHAR(10)), 1, 1) = '5' THEN 'Xirdavat'
        ELSE '-'
    END AS Qol,
    Name AS Kateqoriya
FROM BazarlamaHesabatDB.dbo.ProductGroup
WHERE MikroID NOT IN (0, 999, 521, 601)
ORDER BY MikroID