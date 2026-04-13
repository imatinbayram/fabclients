IF OBJECT_ID('tempdb..#TempReport') IS NOT NULL
    DROP TABLE #TempReport;

CREATE TABLE #TempReport (
    Code NVARCHAR(50),
    Contragent NVARCHAR(100),
    SaleGroup NVARCHAR(100),
    Seller NVARCHAR(100),
    Debt DECIMAL(18,2),
    BottomLimit DECIMAL(18,2),
    TopLimit DECIMAL(18,2),
    Expire NVARCHAR(100),
    ExpiredDebt NVARCHAR(100)  -- əvvəl DECIMAL idi, indi NVARCHAR
)

INSERT INTO #TempReport
    EXEC BazarlamaHesabatDB.[dbo].[Qirmizi_cari]
        @Date = @TarixOlmaz,
        @AnaCari = @Kod

SELECT
    Code CariKod,
    CAST(ExpiredDebt AS DECIMAL(18,2)) Qirmizi
FROM #TempReport
WHERE
    Expire = 'OLMAZ 0'

DROP TABLE #TempReport