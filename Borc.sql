USE MikroDB_V16_05

CREATE TABLE MB_HP (
    CariKod NVARCHAR(50),
    CariAd NVARCHAR(255),
    AnaCariKod NVARCHAR(50),
    AnaCariAd NVARCHAR(255),
    GrupAdi NVARCHAR(255),
    GrupKodu NVARCHAR(50),
    TemsilciKodu NVARCHAR(50),
    TemsilciAdi NVARCHAR(50),
    IlkinQaliq DECIMAL(18,2),
    NetSatis DECIMAL(18,2),
    Medaxil DECIMAL(18,2),
    SonQaliq DECIMAL(18,2)
);

INSERT INTO dbo.MB_HP
EXEC [dbo].[MB_HP_MILTIREP_TEMP] 
    @tarix1,  -- Başlama tarixi
    @tarix2,  -- Bitmə tarixi
    '', '', '',
    @anacari, -- Cari kodu
    '', '', '';

SELECT
    GrupAdi Filial,
    CariAd,
    CariKod,
    SUM(IlkinQaliq) Ilk_Borc,
    SUM(NetSatis) Satis,
    SUM(Medaxil) Medaxil,
    SUM(SonQaliq) Son_Borc,
    SUM(ROUND(ISNULL(Alt_limit, 0), 0)) Alt_limit,
    SUM(ROUND(ISNULL(ct_tutari, 0), 0)) Ust_limit
FROM dbo.MB_HP
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAPLAR ON cari_kod COLLATE SQL_Latin1_General_CP1_CI_AS = CariKod
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAPLAR_USER ON Record_uid = cari_Guid
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAP_TEMINATLARI ON ct_carikodu = cari_kod
WHERE 
TemsilciKodu not IN ('150','160','2000','1020','521')
GROUP BY
    GrupAdi, CariAd, CariKod
ORDER BY
    GrupAdi, CariAd, CariKod DESC

DROP TABLE dbo.MB_HP