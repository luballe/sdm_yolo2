#find /monitoreo/videos/02_Martes/01_AV_JORGE_GAITAN_CORTES_x_AV_BOYACA_SN/results -name 'SN*.csv' | sort |xargs cat > /monitoreo/videos/02_Martes/01_AV_JORGE_GAITAN_CORTES_x_AV_BOYACA_SN/results/SN.csv

#find /monitoreo/videos/02_Martes/02_KR_93_x_AV_J_CELESTINO_MUTIS_WE/results -name 'WE*.csv' | sort |xargs cat > /monitoreo/videos/02_Martes/02_KR_93_x_AV_J_CELESTINO_MUTIS_WE/results/WE.csv
find /monitoreo/videos/02_Martes/03_TV_60_x_AC_127_EW/results -name 'EW*.csv' | sort | xargs cat > /monitoreo/videos/02_Martes/03_TV_60_x_AC_127_EW/results/EW.csv
find /monitoreo/videos/02_Martes/04_AK_72_x_AC_138_SN/results -name 'SN*.csv' | sort | xargs cat > /monitoreo/videos/02_Martes/04_AK_72_x_AC_138_SN/results/SN.csv
find /monitoreo/videos/03_Miercoles/02_AV.AMERICAS_x_KR_53_WE/results -name 'WE*.csv' | sort | xargs cat > /monitoreo/videos/03_Miercoles/02_AV.AMERICAS_x_KR_53_WE/results/WE.csv
find /monitoreo/videos/03_Miercoles/03_KR_91_x_TV_86_NS/results -name 'NS*.csv' | sort | xargs cat > /monitoreo/videos/03_Miercoles/03_KR_91_x_TV_86_NS/results/NS.csv
find /monitoreo/videos/03_Miercoles/04_AK_19_x_AC_127_NS_SN/results -name 'NS*.csv' | sort | xargs cat > /monitoreo/videos/03_Miercoles/04_AK_19_x_AC_127_NS_SN/results/NS.csv
find /monitoreo/videos/03_Miercoles/04_AK_19_x_AC_127_NS_SN/results -name 'SN*.csv' | sort | xargs cat > /monitoreo/videos/03_Miercoles/04_AK_19_x_AC_127_NS_SN/results/SN.csv
find . -name 'NS*.csv' | sort | xargs cat >NSE.csv
