SELECT
    cari_kod Kod, 
    cari_unvan1 Ad, 
    cari_Ana_cari_kodu Ana,
	crg_isim Filial
FROM MikroDB_V16_05.DBO.CARI_HESAPLAR
LEFT JOIN MikroDB_V16_05.DBO.CARI_HESAP_GRUPLARI ON cari_grup_kodu = crg_kod
WHERE
	cari_kod like '120.%'
	and cari_grup_kodu IN ('210','220','230','240','250','520','521','523','540','542','554','555','575')
	and cari_temsilci_kodu IS NOT NULL
	and cari_temsilci_kodu NOT IN ('150','160','2000', '1020')
ORDER BY cari_grup_kodu,cari_unvan1,cari_kod DESC