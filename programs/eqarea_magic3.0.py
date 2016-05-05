#!/usr/bin/env python
import sys
import matplotlib
if matplotlib.get_backend() != "TKAgg":
  matplotlib.use("TKAgg")

import pmagpy.pmag as pmag
import pmagpy.pmagplotlib as pmagplotlib
import new_builder as nb

def main():
    """
    NAME
        eqarea_magic.py

    DESCRIPTION
       makes equal area projections from declination/inclination data

    SYNTAX 
        eqarea_magic.py [command line options]
    
    INPUT 
       takes magic formatted pmag_results, pmag_sites, pmag_samples or pmag_specimens
    
    OPTIONS
        -h prints help message and quits
        -f FILE: specify input magic format file from magic,default='pmag_results.txt'
         supported types=[magic_measurements,pmag_specimens, pmag_samples, pmag_sites, pmag_results, magic_web]
        -obj OBJ: specify  level of plot  [all, sit, sam, spc], default is all
        -crd [s,g,t]: specify coordinate system, [s]pecimen, [g]eographic, [t]ilt adjusted
                default is geographic, unspecified assumed geographic
        -fmt [svg,png,jpg] format for output plots
        -ell [F,K,B,Be,Bv] plot Fisher, Kent, Bingham, Bootstrap ellipses or Boostrap eigenvectors
        -c plot as colour contour 
        -sav save plot and quit quietly
    NOTE
        all: entire file; sit: site; sam: sample; spc: specimen
    """
    FIG={} # plot dictionary
    FIG['eqarea']=1 # eqarea is figure 1
    in_file,plot_key,coord,crd='pmag_results.txt','all',"0",'g'
    plotE,contour=0,0
    dir_path='.'
    fmt='svg'
    verbose=pmagplotlib.verbose
    if '-h' in sys.argv:
        print main.__doc__
        sys.exit()
    if '-WD' in sys.argv:
        ind=sys.argv.index('-WD')
        dir_path=sys.argv[ind+1]
    pmagplotlib.plot_init(FIG['eqarea'],5,5)
    if '-f' in sys.argv:
        ind=sys.argv.index("-f")
        in_file=dir_path+"/"+sys.argv[ind+1]
    if '-obj' in sys.argv:
        ind=sys.argv.index('-obj')
        plot_by=sys.argv[ind+1]
        if plot_by=='all':
          plot_key='all'
        if plot_by=='sit':
          plot_key='site_name'
        if plot_by=='sam':
          plot_key='sample_name'
        if plot_by=='spc':
          plot_key='specimen_name'
    else:
         plot_by = "all" 
    if '-c' in sys.argv:
      contour=1
    plt=0
    if '-sav' in sys.argv: 
        plt=1
        verbose=0
    if '-ell' in sys.argv:
        plotE=1
        ind=sys.argv.index('-ell')
        ell_type=sys.argv[ind+1]
        if ell_type=='F':dist='F' 
        if ell_type=='K':dist='K' 
        if ell_type=='B':dist='B' 
        if ell_type=='Be':dist='BE' 
        if ell_type=='Bv':
            dist='BV' 
            FIG['bdirs']=2
            pmagplotlib.plot_init(FIG['bdirs'],5,5)
    if '-crd' in sys.argv:
        ind=sys.argv.index("-crd")
        crd=sys.argv[ind+1]
        if crd=='s':coord="-1"
        if crd=='g':coord="0"
        if crd=='t':coord="100"
    if '-fmt' in sys.argv:
        ind=sys.argv.index("-fmt")
        fmt=sys.argv[ind+1]

    # all of these are probs wrong....
    Dec_keys=['site_dec','sample_dec','specimen_dec','measurement_dec','average_dec','none']
    Dec_keys = ['dir_dec']
    Inc_keys=['site_inc','sample_inc','specimen_inc','measurement_inc','average_inc','none']
    Inc_keys = ['dir_inc']
    Tilt_keys=['tilt_correction','site_tilt_correction','sample_tilt_correction','specimen_tilt_correction','none']
    Tilt_keys=['dir_tilt_correction']
    Dir_type_keys=['','site_direction_type','sample_direction_type','specimen_direction_type']
    Name_keys=['er_specimen_name','er_sample_name','er_site_name','pmag_result_name']


    data3 = nb.MagicDataFrame(in_file)
    data = data3.df
    
    #data,file_type=pmag.magic_read(in_file)
    #if file_type=='pmag_results' and plot_key!="all":plot_key=plot_key+'s' # need plural for results table
    if verbose:    
        print len(data),' records read from ',in_file
    #
    #
    # find desired dec,inc data:
    #
    dir_type_key=''
    #
    # get plotlist if not plotting all records
    #
    plotlist=[]
    if plot_key!="all":
        # return all where plot_key is not blank
        plots=pmag.get_dictitem(data,plot_key,'','F')
        plots = data[data[plot_key].notnull()]
        #for rec in plots:
        #    if rec[plot_key] not in plotlist:
        #        plotlist.append(rec[plot_key])
        #plotlist.sort()
    #else:
    #    plotlist.append('All')

    if plot_by != "all":
        print "-I- not supporting individual plotting"
        return
    else:
    #for plot in plots.index:
        #print "plots.index", plots.index
        #if True:
        #print 'plotzzz', plot
        #if verbose: print plot
        DIblock=[]
        GCblock=[]
        SLblock,SPblock=[],[]
        title="All"#plot
        mode=1
        dec_key,inc_key,tilt_key,name_key,k="","","","",0
        
        # get all records where dec & inc values exist
        dec_key = Dec_keys[0]
        inc_key = Inc_keys[0]
        data = data[data[dec_key].notnull() & data[inc_key].notnull()]

        tilt_key = Tilt_keys[0] # 'tilt_correction'
        if tilt_key not in data.columns:
            data[tilt_key] = ''

        if coord !='0':
          data = data[data[tilt_key] == coord]
        else: # geographic, include blank records
          data = data[(data[tilt_key] == coord) | (data[tilt_key] == '')]

        print "len(data) equivalent to len(cdata)", len(data)
        #if coord=='0': # geographic
        #    udata=pmag.get_dictitem(Incs,tilt_key,'','T') # get all the blank records - assume geographic
        #    if len(cdata)==0: crd='' 
        #    if len(udata)>0:
        #        for d in udata:cdata.append(d)  
        #        crd=crd+'u'
        #for name_key in Name_keys:
        #    Names=pmag.get_dictitem(cdata,name_key,'','F') # get all records with this name_key not blank 
        #    if len(Names)>0: break
        #print 'name_key', name_key
        #Names = data[data[name_key].notnull()]
        #print Names.index
        
        #for dir_type_key in Dir_type_keys:
        #    Dirs=pmag.get_dictitem(cdata,dir_type_key,'','F') # get all records with this direction type
        #    if len(Dirs)>0: break
        #if dir_type_key=="":dir_type_key='direction_type'
        locations,site,sample,specimen="","","",""

        # DIblock
        # equivalent: DIblock.append([float(rec[dec_key]),float(rec[inc_key])])
        #print data[[dec_key, inc_key]]

        DIblock = [[float(row[dec_key]), float(row[inc_key])] for ind, row in data.iterrows()]
        #print DIblock

        
        if 'magic_method_codes' not in data.columns:
            data['magic_method_codes'] = ''
        #SLblock
        # equivalent SLblock.append([rec[name_key],rec['magic_method_codes']])
        #print data['magic_method_codes']
        SLblock = [[ind, row['magic_method_codes']] for ind, row in data.iterrows()]

        cond = data[tilt_key] == coord # LJ ADD to this cond: rec[dir_type_key] != 'l'.  just don't know what dir_type_key is in 3.0 yet
        #GCblock = [[float(row[dec_key]), float(row[inc_key])] for ind, row in  data[cond].iterrows()]
        GCblock = []
        SPblock = [[ind, row['magic_method_codes']] for ind, row in data[cond].iterrows()]

        print "len(GCblock)", len(GCblock)


        if len(DIblock)>0:
            print 'DIblock is greater than 0'
            if contour==0:
                pmagplotlib.plotEQ(FIG['eqarea'],DIblock,title)
            else:
                pmagplotlib.plotEQcont(FIG['eqarea'],DIblock)
        else:
            print 'DIblock == 0'
            pmagplotlib.plotNET(FIG['eqarea'])


        if len(GCblock)>0:
            print 'GCblock > 0'
            for rec in GCblock:
                pmagplotlib.plotC(FIG['eqarea'],rec,90.,'g')


        if plotE==1:
            print 'plotE', plotE
            ppars=pmag.doprinc(DIblock) # get principal directions
            nDIs,rDIs,npars,rpars=[],[],[],[]
            for rec in DIblock:
                angle=pmag.angle([rec[0],rec[1]],[ppars['dec'],ppars['inc']])
                if angle>90.:
                    rDIs.append(rec)
                else:
                    nDIs.append(rec)
            if dist=='B': # do on whole dataset
                etitle="Bingham confidence ellipse"
                bpars=pmag.dobingham(DIblock)
                for key in bpars.keys():
                    if key!='n' and verbose:print "    ",key, '%7.1f'%(bpars[key])
                    if key=='n' and verbose:print "    ",key, '       %i'%(bpars[key])
                npars.append(bpars['dec']) 
                npars.append(bpars['inc'])
                npars.append(bpars['Zeta']) 
                npars.append(bpars['Zdec']) 
                npars.append(bpars['Zinc'])
                npars.append(bpars['Eta']) 
                npars.append(bpars['Edec']) 
                npars.append(bpars['Einc'])
            if dist=='F':
                etitle="Fisher confidence cone"
                if len(nDIs)>2:
                    fpars=pmag.fisher_mean(nDIs)
                    for key in fpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(fpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(fpars[key])
                    mode+=1
                    npars.append(fpars['dec']) 
                    npars.append(fpars['inc'])
                    npars.append(fpars['alpha95']) # Beta
                    npars.append(fpars['dec']) 
                    isign=abs(fpars['inc'])/fpars['inc'] 
                    npars.append(fpars['inc']-isign*90.) #Beta inc
                    npars.append(fpars['alpha95']) # gamma 
                    npars.append(fpars['dec']+90.) # Beta dec
                    npars.append(0.) #Beta inc
                if len(rDIs)>2:
                    fpars=pmag.fisher_mean(rDIs)
                    if verbose:print "mode ",mode
                    for key in fpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(fpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(fpars[key])
                    mode+=1
                    rpars.append(fpars['dec']) 
                    rpars.append(fpars['inc'])
                    rpars.append(fpars['alpha95']) # Beta
                    rpars.append(fpars['dec']) 
                    isign=abs(fpars['inc'])/fpars['inc'] 
                    rpars.append(fpars['inc']-isign*90.) #Beta inc
                    rpars.append(fpars['alpha95']) # gamma 
                    rpars.append(fpars['dec']+90.) # Beta dec
                    rpars.append(0.) #Beta inc
            if dist=='K':
                etitle="Kent confidence ellipse"
                if len(nDIs)>3:
                    kpars=pmag.dokent(nDIs,len(nDIs))
                    if verbose:print "mode ",mode
                    for key in kpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(kpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(kpars[key])
                    mode+=1
                    npars.append(kpars['dec']) 
                    npars.append(kpars['inc'])
                    npars.append(kpars['Zeta']) 
                    npars.append(kpars['Zdec']) 
                    npars.append(kpars['Zinc'])
                    npars.append(kpars['Eta']) 
                    npars.append(kpars['Edec']) 
                    npars.append(kpars['Einc'])
                if len(rDIs)>3:
                    kpars=pmag.dokent(rDIs,len(rDIs))
                    if verbose:print "mode ",mode
                    for key in kpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(kpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(kpars[key])
                    mode+=1
                    rpars.append(kpars['dec']) 
                    rpars.append(kpars['inc'])
                    rpars.append(kpars['Zeta']) 
                    rpars.append(kpars['Zdec']) 
                    rpars.append(kpars['Zinc'])
                    rpars.append(kpars['Eta']) 
                    rpars.append(kpars['Edec']) 
                    rpars.append(kpars['Einc'])
            else: # assume bootstrap
                if dist=='BE':
                    if len(nDIs)>5:
                        BnDIs=pmag.di_boot(nDIs)
                        Bkpars=pmag.dokent(BnDIs,1.)
                        if verbose:print "mode ",mode
                        for key in Bkpars.keys():
                            if key!='n' and verbose:print "    ",key, '%7.1f'%(Bkpars[key])
                            if key=='n' and verbose:print "    ",key, '       %i'%(Bkpars[key])
                        mode+=1
                        npars.append(Bkpars['dec']) 
                        npars.append(Bkpars['inc'])
                        npars.append(Bkpars['Zeta']) 
                        npars.append(Bkpars['Zdec']) 
                        npars.append(Bkpars['Zinc'])
                        npars.append(Bkpars['Eta']) 
                        npars.append(Bkpars['Edec']) 
                        npars.append(Bkpars['Einc'])
                    if len(rDIs)>5:
                        BrDIs=pmag.di_boot(rDIs)
                        Bkpars=pmag.dokent(BrDIs,1.)
                        if verbose:print "mode ",mode
                        for key in Bkpars.keys():
                            if key!='n' and verbose:print "    ",key, '%7.1f'%(Bkpars[key])
                            if key=='n' and verbose:print "    ",key, '       %i'%(Bkpars[key])
                        mode+=1
                        rpars.append(Bkpars['dec']) 
                        rpars.append(Bkpars['inc'])
                        rpars.append(Bkpars['Zeta']) 
                        rpars.append(Bkpars['Zdec']) 
                        rpars.append(Bkpars['Zinc'])
                        rpars.append(Bkpars['Eta']) 
                        rpars.append(Bkpars['Edec']) 
                        rpars.append(Bkpars['Einc'])
                    etitle="Bootstrapped confidence ellipse"
                elif dist=='BV':
                    sym={'lower':['o','c'],'upper':['o','g'],'size':3,'edgecolor':'face'}
                    if len(nDIs)>5:
                        BnDIs=pmag.di_boot(nDIs)
                        pmagplotlib.plotEQsym(FIG['bdirs'],BnDIs,'Bootstrapped Eigenvectors', sym)
                    if len(rDIs)>5:
                        BrDIs=pmag.di_boot(rDIs)
                        if len(nDIs)>5:  # plot on existing plots
                            pmagplotlib.plotDIsym(FIG['bdirs'],BrDIs,sym)
                        else:
                            pmagplotlib.plotEQ(FIG['bdirs'],BrDIs,'Bootstrapped Eigenvectors')
            if dist=='B':
                if len(nDIs)> 3 or len(rDIs)>3: pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],npars,0)
            elif len(nDIs)>3 and dist!='BV':
                pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],npars,0)
                if len(rDIs)>3:
                    pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],rpars,0)
            elif len(rDIs)>3 and dist!='BV':
                pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],rpars,0)
        if verbose:pmagplotlib.drawFIGS(FIG)
          
        if verbose:
            pmagplotlib.drawFIGS(FIG)
            ans=raw_input(" S[a]ve to save plot, [q]uit, Return to continue:  ")

        return
        
        for rec in cdata: # pick out the data
            if 'er_location_name' in rec.keys() and rec['er_location_name']!="" and rec['er_location_name'] not in locations:locations=locations+rec['er_location_name'].replace("/","")+"_"
            if 'er_location_names' in rec.keys() and rec['er_location_names']!="":
               locs=rec['er_location_names'].split(':')
               for loc in locs:
                   if loc not in locations:locations=locations+loc.replace("/","")+'_'
            if plot_key=='site_name' or plot_key=='sample_name' or plot_key=='specimen_name':
                site=rec['site_name']
            if plot_key=='er_sample_name' or plot_key=='er_specimen_name':
                sample=rec['er_sample_name']
            if plot_key=='er_specimen_name':
                specimen=rec['er_specimen_name']
            if plot_key=='er_site_names' or plot_key=='er_sample_names' or plot_key=='er_specimen_names':
                site=rec['er_site_names']
            if plot_key=='er_sample_names' or plot_key=='er_specimen_names':
                sample=rec['er_sample_names']
            if plot_key=='er_specimen_names':
                specimen=rec['er_specimen_names']
            if dir_type_key not in rec.keys() or rec[dir_type_key]=="":rec[dir_type_key]='l'
            if 'magic_method_codes' not in rec.keys():rec['magic_method_codes']=""
            DIblock.append([float(rec[dec_key]),float(rec[inc_key])])
            SLblock.append([rec[name_key],rec['magic_method_codes']])
            if rec[tilt_key]==coord and rec[dir_type_key]!='l' and rec[dec_key]!="" and rec[inc_key]!="":
                GCblock.append([float(rec[dec_key]),float(rec[inc_key])])
                SPblock.append([rec[name_key],rec['magic_method_codes']])
        if len(DIblock)==0 and len(GCblock)==0:
            if verbose: print "no records for plotting"
            sys.exit()
        if verbose:
          for k in range(len(SLblock)):
            print '%s %s %7.1f %7.1f'%(SLblock[k][0],SLblock[k][1],DIblock[k][0],DIblock[k][1])
          for k in range(len(SPblock)):
            print '%s %s %7.1f %7.1f'%(SPblock[k][0],SPblock[k][1],GCblock[k][0],GCblock[k][1])
        if len(DIblock)>0: 
            if contour==0:
                pmagplotlib.plotEQ(FIG['eqarea'],DIblock,title)
            else:
                pmagplotlib.plotEQcont(FIG['eqarea'],DIblock)
        else:
          pmagplotlib.plotNET(FIG['eqarea'])
        if len(GCblock)>0:
            for rec in GCblock: pmagplotlib.plotC(FIG['eqarea'],rec,90.,'g')
        if plotE==1:
            ppars=pmag.doprinc(DIblock) # get principal directions
            nDIs,rDIs,npars,rpars=[],[],[],[]
            for rec in DIblock:
                angle=pmag.angle([rec[0],rec[1]],[ppars['dec'],ppars['inc']])
                if angle>90.:
                    rDIs.append(rec)
                else:
                    nDIs.append(rec)
            if dist=='B': # do on whole dataset
                etitle="Bingham confidence ellipse"
                bpars=pmag.dobingham(DIblock)
                for key in bpars.keys():
                    if key!='n' and verbose:print "    ",key, '%7.1f'%(bpars[key])
                    if key=='n' and verbose:print "    ",key, '       %i'%(bpars[key])
                npars.append(bpars['dec']) 
                npars.append(bpars['inc'])
                npars.append(bpars['Zeta']) 
                npars.append(bpars['Zdec']) 
                npars.append(bpars['Zinc'])
                npars.append(bpars['Eta']) 
                npars.append(bpars['Edec']) 
                npars.append(bpars['Einc'])
            if dist=='F':
                etitle="Fisher confidence cone"
                if len(nDIs)>2:
                    fpars=pmag.fisher_mean(nDIs)
                    for key in fpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(fpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(fpars[key])
                    mode+=1
                    npars.append(fpars['dec']) 
                    npars.append(fpars['inc'])
                    npars.append(fpars['alpha95']) # Beta
                    npars.append(fpars['dec']) 
                    isign=abs(fpars['inc'])/fpars['inc'] 
                    npars.append(fpars['inc']-isign*90.) #Beta inc
                    npars.append(fpars['alpha95']) # gamma 
                    npars.append(fpars['dec']+90.) # Beta dec
                    npars.append(0.) #Beta inc
                if len(rDIs)>2:
                    fpars=pmag.fisher_mean(rDIs)
                    if verbose:print "mode ",mode
                    for key in fpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(fpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(fpars[key])
                    mode+=1
                    rpars.append(fpars['dec']) 
                    rpars.append(fpars['inc'])
                    rpars.append(fpars['alpha95']) # Beta
                    rpars.append(fpars['dec']) 
                    isign=abs(fpars['inc'])/fpars['inc'] 
                    rpars.append(fpars['inc']-isign*90.) #Beta inc
                    rpars.append(fpars['alpha95']) # gamma 
                    rpars.append(fpars['dec']+90.) # Beta dec
                    rpars.append(0.) #Beta inc
            if dist=='K':
                etitle="Kent confidence ellipse"
                if len(nDIs)>3:
                    kpars=pmag.dokent(nDIs,len(nDIs))
                    if verbose:print "mode ",mode
                    for key in kpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(kpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(kpars[key])
                    mode+=1
                    npars.append(kpars['dec']) 
                    npars.append(kpars['inc'])
                    npars.append(kpars['Zeta']) 
                    npars.append(kpars['Zdec']) 
                    npars.append(kpars['Zinc'])
                    npars.append(kpars['Eta']) 
                    npars.append(kpars['Edec']) 
                    npars.append(kpars['Einc'])
                if len(rDIs)>3:
                    kpars=pmag.dokent(rDIs,len(rDIs))
                    if verbose:print "mode ",mode
                    for key in kpars.keys():
                        if key!='n' and verbose:print "    ",key, '%7.1f'%(kpars[key])
                        if key=='n' and verbose:print "    ",key, '       %i'%(kpars[key])
                    mode+=1
                    rpars.append(kpars['dec']) 
                    rpars.append(kpars['inc'])
                    rpars.append(kpars['Zeta']) 
                    rpars.append(kpars['Zdec']) 
                    rpars.append(kpars['Zinc'])
                    rpars.append(kpars['Eta']) 
                    rpars.append(kpars['Edec']) 
                    rpars.append(kpars['Einc'])
            else: # assume bootstrap
                if dist=='BE':
                    if len(nDIs)>5:
                        BnDIs=pmag.di_boot(nDIs)
                        Bkpars=pmag.dokent(BnDIs,1.)
                        if verbose:print "mode ",mode
                        for key in Bkpars.keys():
                            if key!='n' and verbose:print "    ",key, '%7.1f'%(Bkpars[key])
                            if key=='n' and verbose:print "    ",key, '       %i'%(Bkpars[key])
                        mode+=1
                        npars.append(Bkpars['dec']) 
                        npars.append(Bkpars['inc'])
                        npars.append(Bkpars['Zeta']) 
                        npars.append(Bkpars['Zdec']) 
                        npars.append(Bkpars['Zinc'])
                        npars.append(Bkpars['Eta']) 
                        npars.append(Bkpars['Edec']) 
                        npars.append(Bkpars['Einc'])
                    if len(rDIs)>5:
                        BrDIs=pmag.di_boot(rDIs)
                        Bkpars=pmag.dokent(BrDIs,1.)
                        if verbose:print "mode ",mode
                        for key in Bkpars.keys():
                            if key!='n' and verbose:print "    ",key, '%7.1f'%(Bkpars[key])
                            if key=='n' and verbose:print "    ",key, '       %i'%(Bkpars[key])
                        mode+=1
                        rpars.append(Bkpars['dec']) 
                        rpars.append(Bkpars['inc'])
                        rpars.append(Bkpars['Zeta']) 
                        rpars.append(Bkpars['Zdec']) 
                        rpars.append(Bkpars['Zinc'])
                        rpars.append(Bkpars['Eta']) 
                        rpars.append(Bkpars['Edec']) 
                        rpars.append(Bkpars['Einc'])
                    etitle="Bootstrapped confidence ellipse"
                elif dist=='BV':
                    sym={'lower':['o','c'],'upper':['o','g'],'size':3,'edgecolor':'face'}
                    if len(nDIs)>5:
                        BnDIs=pmag.di_boot(nDIs)
                        pmagplotlib.plotEQsym(FIG['bdirs'],BnDIs,'Bootstrapped Eigenvectors', sym)
                    if len(rDIs)>5:
                        BrDIs=pmag.di_boot(rDIs)
                        if len(nDIs)>5:  # plot on existing plots
                            pmagplotlib.plotDIsym(FIG['bdirs'],BrDIs,sym)
                        else:
                            pmagplotlib.plotEQ(FIG['bdirs'],BrDIs,'Bootstrapped Eigenvectors')
            if dist=='B':
                if len(nDIs)> 3 or len(rDIs)>3: pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],npars,0)
            elif len(nDIs)>3 and dist!='BV':
                pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],npars,0)
                if len(rDIs)>3:
                    pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],rpars,0)
            elif len(rDIs)>3 and dist!='BV':
                pmagplotlib.plotCONF(FIG['eqarea'],etitle,[],rpars,0)
        if verbose:pmagplotlib.drawFIGS(FIG)
            #
        files={}
        locations=locations[:-1]
        for key in FIG.keys():
            filename='LO:_'+locations+'_SI:_'+site+'_SA:_'+sample+'_SP:_'+specimen+'_CO:_'+crd+'_TY:_'+key+'_.'+fmt
            files[key]=filename 
        if pmagplotlib.isServer:
            black     = '#000000'
            purple    = '#800080'
            titles={}
            titles['eq']='Equal Area Plot'
            FIG = pmagplotlib.addBorders(FIG,titles,black,purple)
            pmagplotlib.saveP(FIG,files)
        elif verbose:
            ans=raw_input(" S[a]ve to save plot, [q]uit, Return to continue:  ")
            if ans=="q": sys.exit()
            if ans=="a": pmagplotlib.saveP(FIG,files) 
        if plt:
           pmagplotlib.saveP(FIG,files) 

if __name__ == "__main__":
    main() 