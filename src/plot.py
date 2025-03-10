import numpy
import plotly.express as px
import plotly.io as pio
from pandas import DataFrame, concat
import pprint

class Plot:

    def __init__(self, fig: object):
        
        self.fig = fig

    def __str__(self):
        pass

    @staticmethod
    def set_layout(fig: object) -> object:

        fig.update_layout(
            font=dict(
                size = 15
            ),
            title=dict(
                x = 0.5,
                xanchor= 'center',
                yanchor= 'top'
            )
        )

        return fig
    
class PlotLibrary:

    def __init__(self, file: str):
        
        self.file = file
        self.plots = []

    def __str__(self):
        return f"PlotLibrary with {len(self.plots)} plots"

    def save(self, plot: Plot):
        
        self.plots.append(plot)

    def as_html(self):
         return list(map(lambda p: pio.to_html(p.fig, full_html=False, include_plotlyjs=False),self.plots))

def barplot(data, nominal: str, y: str, color: str, title: str, prefix: str) -> Plot:

    if isinstance(data[0],DataFrame):
        df = concat(data, ignore_index=True)
    elif isinstance(data[0], dict):
        df = DataFrame(data)

    fig = px.bar(data_frame=df, 
                x=nominal, 
                y=y, 
                color=color,
                title=title)
        
    fig.update_xaxes(ticklabelstep=1)
        
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "bar"],
                        label="Bar Chart",
                        method="restyle"
                    )
                ]),
                direction="down",
            ),
        ]
    )

    plot = Plot(fig=fig)

    Plot.set_layout(plot.fig)

    return plot

def histogram(data, x: str, color: str, title: str, prefix: str) -> Plot:

    if isinstance(data[0],DataFrame):
        df = concat(data, ignore_index=True)
    elif isinstance(data[0],dict):
        df = DataFrame(data)

    fig = px.histogram(data_frame=df, x=x, title=title)

    plot = Plot(fig=fig)
    Plot.set_layout(plot.fig)
    return plot

def boxplot(data, nominal: str, y: str, color: str, title: str, prefix: str) -> Plot:

    if isinstance(data[0],DataFrame):
        df = concat(data, ignore_index=True)
    elif isinstance(data[0],dict):
        df = DataFrame(data)

    fig = px.box(data_frame=df,
                    x=nominal,
                    y=y,
                    color=color,
                    title=title)
        
    plot = Plot(fig=fig)
    Plot.set_layout(plot.fig)
    return plot

def venn(self) -> Plot:
    pass


def visualization(file: str, stats: object, library: PlotLibrary):

    data = []

    chromosomes = stats.keys()

    for k in chromosomes:

        data.append({"Chromosome": k, "Type": "Indel", "Count": stats[k]["variant"]["indel"]["deletion"] + stats[k]["variant"]["indel"]["insertion"]})
        data.append({"Chromosome": k, "Type": "SNP", "Count": stats[k]["variant"]["snp"]["transition"] + stats[k]["variant"]["snp"]["transversion"]})
        data.append({"Chromosome": k, "Type": "SV", "Count": stats[k]["variant"]["sv"]})

    library.save(barplot(data,"Chromosome","Count","Type", f"Variant by chromosome {file}", "VariantByChromosome"))

    data.clear()

    for k in chromosomes:
        data.append({"Chromosome": k, "Genotype": "Homozygous", "Count": stats[k]["hom"]})
        data.append({"Chromosome": k, "Genotype": "Heterozygous", "Count": stats[k]["het"]})

    library.save(barplot(data, "Chromosome","Count","Genotype", f"Genotype by chromosome for {file}","GenotypeByChromosome"))

    data.clear()

    chromosome = list(chromosomes)[0]

    if stats[chromosome]["GQ"].size:
        pass

    if stats[chromosome]["depth"].size:

        for k in chromosomes:
            data.append({"Chromosome": k, "Depth": numpy.mean(stats[k]["depth"])})
        
        library.save(barplot(data, "Chromosome", "Depth", color="Chromosome", title=f"Mean depth by chromosome for {file}", prefix="DepthByChromosomeBarPlot"))

        data.clear()

        for k in chromosomes:

            tmp = DataFrame({"Chromosome": [k] * stats[k]["depth"].size,
                                "Depth": stats[k]["depth"].flatten()})

            data.append(tmp)

        library.save(boxplot(data, "Chromosome", "Depth", "Chromosome", f"Depth by chromosome for {file}", "DepthByChromosomeBoxPlot"))

        library.save(histogram(data, "Depth", None, f"Depth for {file}", "DepthHist"))

        data.clear()

    if stats[chromosome]["quality"].size:
        pass