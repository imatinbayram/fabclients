SELECT
	crg_isim Filial,
	cari_Ana_cari_kodu Ana,
    cari_kod Kod, 
    cari_unvan1 Ad
FROM 
    MikroDB_V16_05.DBO.CARI_HESAPLAR
LEFT JOIN
	MikroDB_V16_05.DBO.CARI_HESAP_GRUPLARI
	ON cari_grup_kodu = crg_kod
WHERE
	cari_kod like '120.%'
	AND cari_grup_kodu IN ('210','220','230','240','250','520','521','523','540','542','554','555','575')
	and cari_temsilci_kodu IS NOT NULL
	and cari_temsilci_kodu NOT IN ('150','160','2000', '1020')
ORDER BY cari_grup_kodu,cari_unvan1,cari_kod DESC