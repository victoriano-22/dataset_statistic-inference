# -*- coding: utf-8 -*-

# -- Sheet --

airport = pd.read_csv("dataset")
airport.info()

# airport.dropna(inplace = True)
airport.fillna(airport.mode(), inplace=True)
airport.head()

airport.shape

Q115 = airport[airport["Quarter"].str.contains('1Q15')].reset_index(drop=True)
Q215 = airport[airport["Quarter"].str.contains('2Q15')].reset_index(drop=True)
Q315 = airport[airport["Quarter"].str.contains('3Q15')].reset_index(drop=True)
Q415 = airport[airport["Quarter"].str.contains('4Q15')].reset_index(drop=True)

Q116 = airport[airport["Quarter"].str.contains('1Q16')].reset_index(drop=True)
Q216 = airport[airport["Quarter"].str.contains('2Q16')].reset_index(drop=True)
Q316 = airport[airport["Quarter"].str.contains('3Q16')].reset_index(drop=True)
Q416 = airport[airport["Quarter"].str.contains('4Q16')].reset_index(drop=True)

Q117 = airport[airport["Quarter"].str.contains('1Q17')].reset_index(drop=True)
Q217 = airport[airport["Quarter"].str.contains('2Q17')].reset_index(drop=True)

Q115.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q215.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q315.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q415.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)

Q116.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q216.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q316.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q416.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)

Q117.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)
Q217.drop(['Quarter', 'Date recorded', 'Departure time'], axis=1, inplace=True)

all = [Q115, Q215, Q315, Q415, 
       Q116, Q216, Q316, Q416,
       Q117, Q217]

airportdata = airport.drop(["Quarter", "Date recorded", "Departure time"], axis=1)
airportdata.head()

fig, axes = plt.subplots(len(airportdata.columns)//3, 3, figsize=(12, 48))
axes = axes.flatten()
for col, axis in zip(airportdata.columns, axes):
    sns.distplot(airportdata[col], ax=axis)

# Diketahui bahwa untuk kolom target, ada banyak yang tidak berdistribusi normal karena ini hanya sample. Karena itu, kita harus menggunakan t square untuk mendapat rataan dan chi square untuk mendapat standard deviasi dari setiap kolom target.


def stat_inference(col, n, dof, p):

    samplemean = col.mean()
    samplestd = col.std()

    sample_squared = col**2
    sum_sample_squared = sample_squared.sum()
    sum_sample = col.sum()
    squared_sum_sample = sum_sample**2
    variance = (n*sum_sample_squared - squared_sum_sample) / (n*dof)

    lowmean, highmean, nilai_t = ttest(n, p, dof, samplemean, samplestd)
    lowvar, highvar = chisquare(n, dof, variance)

    return lowmean, lowvar, highmean, highvar, nilai_t

def ttest(n, p, dof, mean, std):
    t_value = t.ppf(p, dof)
    # p = t.cdf(t_value, dof)
    margin_of_error = t_value * std / np.sqrt(n)
    
    lowbound = mean - margin_of_error
    upbound = mean + margin_of_error

    return lowbound, upbound, t_value

def chisquare(n, dof, vari):
    p1 = 0.975
    chi_value_0975 = chi2.ppf(p1, dof)

    p2 = 0.025
    chi_value_0025 = chi2.ppf(p2, dof)

    lowbound = (n - 1)*vari/chi_value_0975
    upbound = (n - 1)*vari/chi_value_0025

    return lowbound, upbound

def cal_thresh(df, colum, number):
    count=df.loc[:,colum]
    count=count[~ (count<=number)] 
    count=count.shape[0]
    return count

colist = Q115.columns.to_list()
p = 0.975
finaldict = {}
s = {}
var = {}
htf = {}
quarter = 1
year = 2015
for i in range(len(all)):
    num_sample = all[i].shape[0]
    deg = num_sample - 1
    templist = []
    templist2 = []
    templist3 = []
    templist4 = []
    if quarter > 4:
        quarter = 1
        year += 1
    if num_sample > 0:
        sentence = str(year) + "Q" + str(quarter)
        for columns in colist:
            low_mean, low_var, high_mean, high_var, t_val = stat_inference(all[i][columns], num_sample, deg, p)
            templist.append([low_mean, high_mean, low_var, high_var])
            templist2.append(low_mean)
            templist3.append(high_var + low_var)
            templist4.append(cal_thresh(all[i], columns, 4))
        finaldict[sentence] = templist
        s[sentence] = templist2
        var[sentence] = templist3
        htf[sentence] = templist4
    quarter += 1

#inferensi statistika per kuartil
finaldf = pd.DataFrame.from_dict(finaldict, orient='index', columns=colist)
finaldf.head(16)

#lower bound
s_df = pd.DataFrame.from_dict(s, orient='index', columns=colist)
s_df.head(16)

#jumlah dari batas atas dan bawah variansi
var_df = pd.DataFrame.from_dict(var, orient='index', columns=colist)
var_df.head(16)

#lebih dari atau sama dengan 4
htf_df = pd.DataFrame.from_dict(htf, orient='index', columns=colist)
htf_df.head(16)

sns.set(rc={'figure.figsize':(15,15)})
quarter = finaldf.index.values
y = finaldf["Arrivals passport and visa inspection"].map(lambda x: x[0])
z = finaldf["Arrivals passport and visa inspection"].map(lambda x: x[1])

a = finaldf["Cleanliness of airport terminal"].map(lambda x: x[0])
b = finaldf["Cleanliness of airport terminal"].map(lambda x: x[1])

c = finaldf["Shopping facilities"].map(lambda x: x[0])
d = finaldf["Shopping facilities"].map(lambda x: x[1])

fig, ax = plt.subplots(3,1)
ax[0].bar(quarter, z, width=0.2,align='edge', color = 'b')
ax[0].bar(quarter, y, width=-0.2, align='edge', color = 'g')
ax[0].set_ylabel('Satisfaction Arrivals Inspection')

ax[1].bar(quarter, b, width=0.2,align='edge', color = 'b')
ax[1].bar(quarter, a, width=-0.2, align='edge', color = 'g')
ax[1].set_ylabel('Satisfaction Cleanliness')

ax[2].bar(quarter, d, width=0.2,align='edge', color = 'b')
ax[2].bar(quarter, c, width=-0.2, align='edge', color = 'g')
ax[2].set_ylabel('Satisfaction Shopping Facilities')

ax[0].legend(['High Mean', 'Low Mean'])
ax[1].legend(['High Mean', 'Low Mean'])
ax[2].legend(['High Mean', 'Low Mean'])
fig.suptitle('Rataan per Kuartil', fontsize=16)
plt.show()

# import plotly.graph_objects as go

# quarter = finaldf.index.values

# open_data = finaldf["Arrivals passport and visa inspection"].map(lambda x: x[0])
# high_data = finaldf["Arrivals passport and visa inspection"].map(lambda x: x[1])
# low_data = open_data - finaldf["Arrivals passport and visa inspection"].map(lambda x: np.sqrt(x[2]))
# close_data = high_data + finaldf["Arrivals passport and visa inspection"].map(lambda x: np.sqrt(x[3]))
# dates = quarter

# fig = go.Figure(data=[go.Candlestick(x=quarter,
#                        open=open_data, high=high_data,
#                        low=low_data, close=close_data)])

# fig.show()

# <h1> Jawaban untuk inferensi statistika


# <h1> A - Batas bawah kepuasan layanan


# Batas bawah = low_mean - tvalue * low_std / sqrt(n)
# p = 0.025, dof = n-1   


s_df.loc["mean"] = s_df.mean()

s_df_mean = s_df.mean().to_frame()

s_df_mean = s_df_mean.rename(columns = {0: 'Average Low Limit of Services'}, inplace = False)

sns.set(rc={'figure.figsize':(18,7)})
s_df_mean.plot.bar(xlabel='Airport Services')

s_df_mean.add

# <h1> B - Banyaknya responden yang puas
# <!-- <h5> Manajemen mengasumsikan bahwa seseorang tergolong‘puas‘ terhadap suatu layanan jika ia mengisi skor lebih besar atau sama dengan 4. Berikan inferensi statistika untuk proporsi banyaknya responden yang tergolong ‘puas‘ terhadap layanan yang Anda analisis. -->


size = airportdata.shape[0]
htf_stat = {}
temp = []
quarter = 1
year = 2015

for columns in colist:
    lm, lv, hm, hv, tval = stat_inference(htf_df[columns], size, size-1, p)
    temp.append([lm, hm, lv, hv])
htf_stat["final"] = temp

htf_stat_df = pd.DataFrame.from_dict(htf_stat, orient='index', columns=colist)
htf_stat_df.head(16)

htf_mean = htf_stat_df.loc["final"].map(lambda x: x[0])
htf_mean = htf_mean.to_frame()

htf_mean = htf_mean.rename(columns = {'final': 'Average Num of Satisfied People'}, inplace = False)

sns.set(rc={'figure.figsize':(18,7)})
htf_mean.plot.bar(xlabel='Airport Services')

htf_mean.add

# <h1> C - Keseragaman/kevariativan Layanan


tes = var_df.mean().mean()
tes

threshold = tes
variatif = var_df[(var_df > threshold)]
variatif        

# 


seragam = var_df[(var_df < threshold)]
seragam

var_df_mean = var_df.mean().to_frame()

var_df_mean = var_df_mean.rename(columns = {0: 'Average Num of Variance Sum'}, inplace = False)

var_df_mean.plot.bar(xlabel='Airport Services')

var_df_mean.head(36)

# <h1> D - Layanan yang harus didampingi


# Dari hasil diskusi A, B dan C maka kami membandingkan 2 layanan yang memiliki Batas bawah rating terendah dan kepuasan terendah. Layanan tersebut adalah <b> Ease of Making connections </b> dan <b> Business/Executive Lounges </b>


s_df_mean.plot.bar(xlabel='Airport Services')
var_df_mean.plot.bar(xlabel='Airport Services')
sns.set(rc={'figure.figsize':(18,7)})
htf_mean.plot.bar(xlabel='Airport Services')

# Kemudian dari antara 2 layanan tersebut kami memilih yang variansinya lebih kecil


# Kami akhirnya memiliki <b> Ease of Making Connections </b> Untuk mendapatkan pendampingan khusus dari manajemen




