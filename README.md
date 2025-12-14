# Bike Sharing Dashboard
Bike Sharing merupakan generasi baru dari penyewaan sepeda tradisional, di mana seluruh proses mulai dari keanggotaan, peminjaman, hingga pengembalian sepeda telah dilakukan secara otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari suatu lokasi tertentu dan mengembalikannya di lokasi lain. Saat ini, terdapat lebih dari 500 program berbagi sepeda di seluruh dunia yang mencakup lebih dari 500 ribu unit sepeda. Dewasa ini, sistem-sistem tersebut mendapat perhatian besar karena perannya yang penting dalam isu lalu lintas, lingkungan, dan kesehatan.

Selain memiliki aplikasi nyata yang menarik, karakteristik data yang dihasilkan oleh sistem bike sharing juga menjadikannya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan serta lokasi keberangkatan dan kedatangan dicatat secara eksplisit dalam sistem ini. Fitur ini menjadikan bike sharing sebagai sebuah jaringan sensor virtual yang dapat digunakan untuk memantau mobilitas di dalam kota. Oleh karena itu, diharapkan bahwa sebagian besar peristiwa penting di suatu kota dapat dideteksi melalui pemantauan data tersebut.

## Dataset
Dataset utama yang digunakan berkaitan dengan catatan historis selama dua tahun, yaitu tahun 2011 dan 2012, dari sistem Capital Bikeshare di Washington D.C., Amerika Serikat, yang tersedia untuk umum di http://capitalbikeshare.com/system-data. Data tersebut kemudian diagregasi dalam basis per jam dan harian, lalu dilengkapi dengan informasi cuaca dan musiman yang sesuai. Informasi cuaca diperoleh dari http://www.freemeteo.com.

## Hasil Analisis
Analisis dilakukan dengan menggunakan Python melalui Colab. Dari proses analisis, diperoleh kesimpulan sebagai berikut:
- Menjelang akhir pekan yaitu pada hari Kamis, Jumat dan Sabtu pada jam 17.00-18.00 terjadi kenaikan jumlah pengguna bike-sharing dibandingkan hari-hari dan jam-jam yang lainnya.
- Terjadi kenaikan jumlah pengguna bike-sharing yang cukup signifikan dari tahun 2011 ke tahun 2012 yaitu sekitar 1 juta pengguna
- Mayoritas pengguna bike-sharing melakukan penyewaan sepeda pada musim gugur, ketika cuaca sedang cerah, sedikit awan ataupun berawan sebagian.
- Mayoritas pengguna bike-sharing melakukan penyewaan ketika hari kerja dan bukan hari libur

Untuk lebih jelasnya dapat dilihat [disini](bike_sharing_analysis.ipynb).

## Dashboard
Untuk melihat hasil visualisasi data dalam bentuk dashboard, ada dua cara sebagai berikut:
### Akses dashboard online di Streamlit Cloud
[Klik di sini untuk melihat dashboard](https://bikesharing-dashboardd.streamlit.app/).

### Run di Lokal
1. Clone repository
2. Install library yang dibutuhkan
3. Jalankan dashboard, ketik pada terminal sebagai berikut
   "streamlit run bike_sharing_db.py"

## Dependencies
- Python 3.x
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- Babel

## Catatan
- Pastikan semua file CSV ada di folder 'data/'
- Dashboard di Streamlit Cloud otomatis redeploy jika ada perubahan di Github.
