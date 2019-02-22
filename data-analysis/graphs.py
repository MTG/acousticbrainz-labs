import matplotlib.colors as clr
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import squarify 

def init_setup():

    sns.set(rc={'figure.figsize':(15,8)})
    sns.set(style="white", context="talk")


def genre_pie(genre_counts, genre_list, name):

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(genre_counts)

    #Compute percentages
    pct = 100*genre_counts/len(genre_list)

    ax.legend(labels=['%s  %1.2f %%' % (l, s) for l, s in zip(list(pct.keys()), list(pct))], loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title(name)
    plt.show()
    
    
def genre_bar(genre_counts, genre_list, name): 
    
    total = float(len(genre_list))
    ax = sns.barplot(x=genre_counts, y=genre_counts.keys(), orient='h', palette='PuBu_r')

    #Compute and locate percentages
    for p in ax.patches:
        loc = ax.patches[0].get_width()
        width = p.get_width()
        ax.text(loc+ 20, p.get_y()+p.get_height()/1.5, '  '+'{:1.2f}'.format(100*width/total) + '%', ha='left') 
        
    ax.set_xticks([])
    sns.despine(left=True, bottom=True)
    plt.show()


def genre_map(genre_counts, genre_list, name, th):

    # Creating colorscheme
    cmap = cm.Blues
    mini=min(np.array(genre_counts))
    maxi=max(np.array(genre_counts))
    norm = clr.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in np.array(genre_counts)]

    other = 0
    x = np.array(genre_counts)
    y = np.array(genre_counts.keys())

    if th > 0:
        for el in x:
            
            pct = 100*el/float(len(genre_list))
            
            if pct < th:
                other += el
                i = np.where(x == el)
                x = np.delete(x, i, 0)
                y = np.delete(y, i, 0)
                
        x = np.append(x, other)
        y = np.append(y, 'other')

    squarify.plot(sizes=x, label=y, alpha=.8, color=colors)
    plt.axis('off')
    plt.title(name)
    plt.show() 