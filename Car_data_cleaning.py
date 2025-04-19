
import pandas as pd
import numpy as np
data = pd.read_csv('intern_car_regg.csv')
data.columns = data.columns.str.strip() #Columnlardakı potensial boşluqlar silinir.
import seaborn as sns

data.drop(columns=['Avtosalon','Şəhər','Yeni','Yeniləndi','Baxışların sayı','Etrafli','Sahiblər','Yerlərin sayı','Qəzalı'],inplace=True) # Lazımsız columnlar silinir.
data['Qiymet'] = data['Qiymet'].astype(float) # Burda 'float'-a çevirməyimin səbəbi 1.7 və 1.9-a vurmağımdır çünki columnu int typeda olan vaxtı bu ədədlərə vuranda 'warning' ortaya çıxır.
data.loc[data['Valyuta'] == 'USD' ,'Qiymet'] = data.loc[data['Valyuta'] == 'USD' ,'Qiymet'] * 1.7 # data.loc ilə 'Valyuta'-sı 'USD' olan 'Qiymet'-ləri filtrlənib tapıldıqdan sonra 1.7-ə vurub 'AZN'-ə çevrilir.
data.loc[data['Valyuta'] == 'EUR' ,'Qiymet'] = data.loc[data['Valyuta'] == 'EUR' ,'Qiymet'] * 1.9 #Eyni prosesi 'Valyuta'-sı 'EUR' olanlar üçün edilir.
data.drop(columns = 'Valyuta',inplace=True) # Artıq bütün qiymətlərin valyutası 'AZN' olduğu üçün 'Valyuta' columnunun əhəmiyyəti qalmır və bu column silinir.
data['Qiymet'] = data['Qiymet'].astype(int) # 'Qiymet' columnunun dəyərləri int formasında olmalıdır deyə və əvvəldə vurma əməliyyatı zamanı floata çevirdiyim üçün yenidın 'int'-ə çevirdim.
data.rename(columns = {'Qiymet' : 'Qiymet(AZN)'},inplace=True) # Valyutaların hamısı 'AZN' olduğu üçün 'Qiymet(AZN)' adı datanı oxuyanlar üçün də daha anlaşıqlı olar deyə columnun adını dəyişdim.

data[['Mühərrikin həcmi(Litr)','At gücü','Yanacaq növü']] = data['Mühərrik'].str.split('/',expand=True) # 'Mühərrik' columnu özündə müxtəlif məlumatlar daşıyır və bu məlumatlar müxtəlif columnlarda qeyd oluna bilər deyə 'str.split' metodundan istifadə edərək 'Mühərrik' columnunu 3 fərqlo columna ayırdım.
data['Mühərrikin həcmi(Litr)'] = data['Mühərrikin həcmi(Litr)'].str[:-2].str.strip().astype(float) # 'Mühərrikin həcmi(Litr)' columnu 'float' type-da olmalıdır,bunun üçün də str[:-2]-dən istifadə etdim ki ' L' hissəsi nəzərə alınmasın və columnu numeric type-a çevirim.
data['At gücü'] = data['At gücü'].str[:-4].str.strip().astype(int) # Eyni proses 'At gücü' columnu üçün təkrar olunur.
data.drop(columns = 'Mühərrik',inplace=True) # Split edildikdən sonra 'Mühərrik' columnunun mənası qalmır və silinir.
data[['Zədə durumu','Boya müdaxiləsi']] = data['Vəziyyəti'].str.split(',',expand=True) # 'Vəziyyəti' columnu da 2 fərqli columna ayrılır.
data.drop(columns = 'Vəziyyəti',inplace=True) # 'Mühərrik' columnu kimi bu column da silinir.
data['Boya müdaxiləsi'] = data['Boya müdaxiləsi'].str.strip().str.capitalize() # Ilk hərf böyük olsun deyə bu üsuldan istifadə etmişəm(sadəcə daha səliqəli görünsün deyə bunu etdim).
data['Zədə durumu'] = data['Zədə durumu'].str.strip()


data['Yürüş'] = data['Yürüş'].str[:-2].str.strip() # 'Yürüş' columnunu numeric type etmək üçün də eyni proses təkrar olunur('km' hissəsi silinir).
data['Yürüş'] = data['Yürüş'].str.replace(" ", "").astype(int) # Sadəcə 'km' silinməsi kifayət etmir,space-lər də silinir ki numeric type-a çevrilmə mümkün olsun.
data.rename(columns={'Yürüş' : 'Yürüş(Km)'},inplace=True) # 'Qiymet' sütununda olduğu kimi 'Yürüş' sütununda da məlumatın daha anlaşılan olması üçün 'rename' edirəm.

data['len'] = data['Extra'].apply(lambda x : len(str(x)))
data['len'] # 'Extra' columnunun bölünməsi fərqli olacağı üçün uzunluğu ən uzun olan rowu tapıb ona əsasən yeni columnlar yaradılacaq.

data[data['len'] == 213] # Max uzunluq 213 olduğu üçün uzunluğu 213 olan rowlar tapılır.

data.loc[8:8,'Extra'].unique() # Uzunluğu 213 olnlardan istənilən biri götürülür və unique dəyərləri tapılır

data['Yüngül lehimli disklər'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Yüngül lehimli disklər' in x else 'yox')
data['ABS'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'ABS' in x else 'yox')
data['Lyuk'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Lyuk' in x else 'yox')
data['Yağış sensoru'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Yağış sensoru' in x else 'yox')
data['Mərkəzi qapanma'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Mərkəzi qapanma' in x else 'yox')
data['Park radarı'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Park radarı' in x else 'yox')
data['Kondisioner'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Kondisioner' in x else 'yox')
data['Oturacaqların isidilməsi'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Oturacaqların isidilməsi' in x else 'yox')
data['Dəri salon'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Dəri salon' in x else 'yox')
data['Ksenon lampalar'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Ksenon lampalar' in x else 'yox')
data['Arxa görüntü kamerası'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Arxa görüntü kamerası' in x else 'yox')
data['Yan pərdələr'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Yan pərdələr' in x else 'yox')
data['Oturacaqların ventilyasiyası'] = data.Extra.apply(lambda x:np.nan if pd.isna(x) else 'var' if 'Oturacaqların ventilyasiyası' in x else 'yox')
data.drop(columns={'Extra','len'},inplace=True) # Ənənəvi olaraq column split olunduqdan sonra silinir.

data.isnull().sum()

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='most_frequent')
data['Hansı bazar üçün yığılıb'] = imputer.fit_transform(data[['Hansı bazar üçün yığılıb']]).ravel()
data['Zədə durumu'] = imputer.fit_transform(data[['Zədə durumu']]).ravel()
data['Boya müdaxiləsi'] = imputer.fit_transform(data[['Boya müdaxiləsi']]).ravel()

data['Yüngül lehimli disklər'] = data['Yüngül lehimli disklər'].replace({np.nan : 'yox'})
data['ABS'] = data['ABS'].replace({np.nan : 'yox'})
data['Lyuk'] = data['Lyuk'].replace({np.nan : 'yox'})
data['Yağış sensoru'] = data['Yağış sensoru'].replace({np.nan : 'yox'})
data['Mərkəzi qapanma'] = data['Mərkəzi qapanma'].replace({np.nan : 'yox'})
data['Park radarı'] = data['Park radarı'].replace({np.nan : 'yox'})
data['Kondisioner'] = data['Kondisioner'].replace({np.nan : 'yox'})
data['Oturacaqların isidilməsi'] = data['Oturacaqların isidilməsi'].replace({np.nan : 'yox'})
data['Dəri salon'] = data['Dəri salon'].replace({np.nan : 'yox'})
data['Ksenon lampalar'] = data['Ksenon lampalar'].replace({np.nan : 'yox'})
data['Arxa görüntü kamerası'] = data['Arxa görüntü kamerası'].replace({np.nan : 'yox'})
data['Yan pərdələr'] = data['Yan pərdələr'].replace({np.nan : 'yox'})
data['Oturacaqların ventilyasiyası'] = data['Oturacaqların ventilyasiyası'].replace({np.nan : 'yox'})
data.isnull().sum()

sns.heatmap(data.drop(columns=['Qiymet(AZN)']).select_dtypes(include= 'number').corr() , annot=True)


data.select_dtypes(include=['number']).plot.box(vert = False)

Q1 = data['At gücü'].quantile(0.25)
Q2 = data['At gücü'].quantile(0.75)
IQR = Q2 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q2 + 1.5 * IQR
data['At gücü'] = data['At gücü'].clip(lower = lower_bound, upper = upper_bound)

Q1 = data['Mühərrikin həcmi(Litr)'].quantile(0.25)
Q2 = data['Mühərrikin həcmi(Litr)'].quantile(0.75)
IQR = Q2 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q2 + 1.5 * IQR
data['Mühərrikin həcmi(Litr)'] = data['Mühərrikin həcmi(Litr)'].clip(lower = lower_bound, upper = upper_bound)

Q1 = data['Yürüş(Km)'].quantile(0.25)
Q2 = data['Yürüş(Km)'].quantile(0.75)
IQR = Q2 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q2 + 1.5 * IQR
data['Yürüş(Km)'] = data['Yürüş(Km)'].clip(lower = lower_bound, upper = upper_bound)

Q1 = data['Buraxılış ili'].quantile(0.25)
Q2 = data['Buraxılış ili'].quantile(0.75)
IQR = Q2 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q2 + 1.5 * IQR
data['Buraxılış ili'] = data['Buraxılış ili'].clip(lower = lower_bound, upper = upper_bound)

Q1 = data['Qiymet(AZN)'].quantile(0.25)
Q2 = data['Qiymet(AZN)'].quantile(0.75)
IQR = Q2 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q2 + 1.5 * IQR
data['Qiymet(AZN)'] = data['Qiymet(AZN)'].clip(lower = lower_bound, upper = upper_bound)

data.select_dtypes(include=['number']).plot.box(vert = False)
data.head()
