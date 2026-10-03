"""Gráficos acadêmicos: SVG vetorial versionado e PNG 180 dpi na execução."""
import logging
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .config import ROOT

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                     'figure.dpi':110,'savefig.dpi':180,'svg.fonttype':'none'})

def save(fig, chapter: str, name: str):
    folder=ROOT/'outputs/figures'/chapter; folder.mkdir(parents=True,exist_ok=True)
    fig.text(.01,.006,'Fonte: Google Meridian · dados simulados · análise descritiva',fontsize=7,color='#555555')
    fig.tight_layout(rect=(0,.025,1,1))
    for suffix in ['svg','png']:
        path=folder/f'{name}.{suffix}'
        fig.savefig(path,bbox_inches='tight')
        logging.info('Figura: %s',path)
    plt.close(fig)
    return folder/f'{name}.png'

def heatmap(frame,chapter,name,title,cmap='viridis',vmin=None,vmax=None):
    fig,ax=plt.subplots(figsize=(13,max(4,min(12,len(frame)*.23))))
    im=ax.imshow(frame.to_numpy(dtype=float),aspect='auto',cmap=cmap,vmin=vmin,vmax=vmax,interpolation='nearest')
    ax.set_yticks(np.arange(len(frame)),frame.index.astype(str),fontsize=7)
    n=len(frame.columns); ticks=np.unique(np.linspace(0,n-1,min(n,12)).astype(int))
    ax.set_xticks(ticks,[str(frame.columns[i])[:10] for i in ticks],rotation=45,ha='right',fontsize=8)
    ax.set_title(title); ax.set_xlabel(frame.columns.name or 'Variável / período');ax.set_ylabel(frame.index.name or 'Variável / GEO')
    fig.colorbar(im,ax=ax,shrink=.75)
    return save(fig,chapter,name)

def bars(series,chapter,name,title,ylabel):
    fig,ax=plt.subplots(figsize=(max(8,len(series)*.22),4.8))
    series.plot.bar(ax=ax,color='#245b78');ax.set_title(title);ax.set_ylabel(ylabel)
    ax.tick_params(axis='x',labelsize=8)
    return save(fig,chapter,name)

def lines(frame,chapter,name,title,ylabel):
    fig,ax=plt.subplots(figsize=(12,4))
    xlabel={'time':'Semana','rank':'Posição no ranking de geos','lag_weeks':'Defasagem (semanas)'}.get(frame.index.name,frame.index.name or 'Semana')
    frame.plot(ax=ax);ax.set_title(title);ax.set_ylabel(ylabel);ax.set_xlabel(xlabel)
    return save(fig,chapter,name)

def scatter(x,y,chapter,name,title,xlabel,ylabel):
    fig,ax=plt.subplots(figsize=(6.5,5))
    ax.scatter(x,y,s=28,alpha=.7);ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    return save(fig,chapter,name)
