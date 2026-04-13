SELECT
    cari_kod,
    ROUND(ISNULL(Alt_limit, 0), 0) Alt_limit,
    ROUND(ISNULL(ct_tutari, 0), 0) Ust_limit
FROM CARI_HESAPLAR
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAPLAR_USER ON Record_uid = cari_Guid
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAP_TEMINATLARI ON ct_carikodu = cari_kod
WHERE
    cari_Ana_cari_kodu = @anacari
ORDER BY cari_kod DESC