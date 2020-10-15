import pandas as pd
import numpy as np
import wquantiles as w
import functions as f

l = ['2012','2013','20142015','2016','2017']
results = pd.DataFrame(index = list(range(2012,2018)))

for i in range(2012, 2018):
    df = pd.read_csv(r'C:\Backup\I & E Surveys\\' + str(i) + '\CSV\MB_' + str(i)+'.csv')
    results.loc[i, 'mean'] = np.average(df['net'], weights = df['weight'])
    results.loc[i, 'mean to nefesh'] = np.average(df['net']/df['nefashot'], weights = df['weight'])
    
    df['net_to_nefesh'] = df['net']/df['nefeshstandartit']
    df['bruto_to_nefesh'] = df['i1kaspit']/df['nefeshstandartit']
    df['bruto_colelet_to_nefesh'] = (df['i1kaspit'] + df['iinkind'])/df['nefeshstandartit']
    df['total_to_nefesh'] = df['total_net']/df['nefeshstandartit']
    
    df['weight_nefesh'] = df['weight']*df['nefashot']
    
    oni_threshold_i = w.median(df['net_to_nefesh'], df['weight'])/2
    oni_threshold_ii = w.median(df['bruto_to_nefesh'], df['weight'])/2
    oni_threshold_iii = w.median(df['bruto_colelet_to_nefesh'], df['weight'])/2
    oni_threshold_iv = w.median(df['total_to_nefesh'], df['weight'])/2
    
    results.loc[i, 'oni_i_hb'] = df[df['net_to_nefesh'] < oni_threshold_i]['weight'].sum()/df['weight'].sum()
    results.loc[i, 'oni_i_nefashot'] = df[df['net_to_nefesh'] < oni_threshold_i]['weight_nefesh'].sum()/df['weight_nefesh'].sum()
    
    results.loc[i, 'oni_ii_hb'] = df[df['bruto_to_nefesh'] < oni_threshold_ii]['weight'].sum()/df['weight'].sum()
    results.loc[i, 'oni_ii_nefashot'] = df[df['bruto_to_nefesh'] < oni_threshold_ii]['weight_nefesh'].sum()/df['weight_nefesh'].sum()
    
    results.loc[i, 'oni_iii_hb'] = df[df['bruto_colelet_to_nefesh'] < oni_threshold_iii]['weight'].sum()/df['weight'].sum()
    results.loc[i, 'oni_iii_nefashot'] = df[df['bruto_colelet_to_nefesh'] < oni_threshold_iii]['weight_nefesh'].sum()/df['weight_nefesh'].sum()
    
    results.loc[i, 'oni_iv_hb'] = df[df['total_to_nefesh'] < oni_threshold_iv]['weight'].sum()/df['weight'].sum()
    results.loc[i, 'oni_iv_nefashot'] = df[df['total_to_nefesh'] < oni_threshold_iv]['weight_nefesh'].sum()/df['weight_nefesh'].sum()
    
for i in l:
    df = pd.read_csv(r'C:\Users\User\Documents\Projects\Pension\\' + i + '\CSV\MB_' + i + '.csv', encoding = "ISO-8859-1", low_memory = False)
    df['nefeshstandartit'] = df['SachNefashot'].apply(f.nefesh_btl)
    df['bruto_to_nefesh'] = df['SacShnatikolel_Lembnew']/df['nefeshstandartit']
    df['weight_nefesh'] = df['MishkalMb']*df['SachNefashot']
    
    oni_threshold_ii = w.median(df['bruto_to_nefesh'], df['MishkalMb'])/2
    if i == '20142015':
        results.loc[2014, 'orech_oni_ii_hb'] = df[df['bruto_to_nefesh'] < oni_threshold_ii]['MishkalMb'].sum()/df['MishkalMb'].sum()
        results.loc[2014, 'orech_oni_ii_nefashot'] = df[df['bruto_to_nefesh'] < oni_threshold_ii]['weight_nefesh'].sum()/df['weight_nefesh'].sum()
    else:
        results.loc[int(i), 'orech_oni_ii_hb'] = df[df['bruto_to_nefesh'] < oni_threshold_ii]['MishkalMb'].sum()/df['MishkalMb'].sum()
        results.loc[int(i), 'orech_oni_ii_nefashot'] = df[df['bruto_to_nefesh'] < oni_threshold_ii]['weight_nefesh'].sum()/df['weight_nefesh'].sum()

results.to_csv(r'C:\Users\User\Documents\Projects\oni_script_results.csv')  