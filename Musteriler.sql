SELECT
    cari_kod Kod, 
    cari_unvan1 Ad, 
    cari_Ana_cari_kodu Ana,
	crg_isim Filial,
--	crg_kod,
	cari_temsilci_kodu,
	cari_per_adi,
--	cari_cari_kilitli_flg,
--	cari_create_date,
--	cari_banka_hesapno1,
--	MAIN.[Name] SEBEKE,
	isnull(adr_ziyaretgunu,0) rut,
	cari_sektor_kodu,
	isnull(adr_gps_boylam,0) adr_gps_boylam,
	isnull(adr_gps_enlem,0) adr_gps_enlem,
	ROUND(ISNULL(Alt_limit, 0), 0) Alt,
	ROUND(ISNULL(ct_tutari, 0), 0) Ust
FROM MikroDB_V16_05.DBO.CARI_HESAPLAR
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAP_GRUPLARI ON cari_grup_kodu = crg_kod
LEFT JOIN MikroDB_V16_05.DBO.CARI_PERSONEL_TANIMLARI ON cari_temsilci_kodu = cari_per_kod
--LEFT JOIN BazarlamaHesabatDB.dbo.ContragentInfo CI WITH(NOLOCK) ON cari_Ana_cari_kodu COLLATE SQL_Latin1_General_CP1_CI_AS = CI.ContragentCode
--LEFT JOIN BazarlamaHesabatDB.dbo.MainContragent MAIN WITH(NOLOCK) ON CI.MainContragentOid = MAIN.Oid
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAP_ADRESLERI on adr_cari_kod = cari_kod
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAPLAR_USER ON Record_uid = cari_Guid
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAP_TEMINATLARI ON ct_carikodu = cari_kod
WHERE
	cari_kod like '120.%'
	and cari_grup_kodu IN ('210','220','230','240','250','520','521','523','540','542','554','555','575')
	and cari_temsilci_kodu IS NOT NULL
	and cari_temsilci_kodu NOT IN ('150','160','2000', '1020')
ORDER BY cari_grup_kodu,cari_unvan1,cari_sektor_kodu