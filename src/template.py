from jinja2 import Environment, FileSystemLoader
from pandas import isna

class Report:

    def __init__(self, vcfs: list[str], infos, df, plots):

        self.vcfs = vcfs

        self.infos = infos
        
        self.data = df

        self.plots = plots

    def __str__(self):
        pass

    def create(self):

        def is_nan(value):
            return isna(value)
        
        env = Environment(loader=FileSystemLoader('src/templates'))

        env.filters['is_nan'] = is_nan

        template = env.get_template("template.html")

        html = template.render(vcfs=self.vcfs, infos=self.infos, df=self.data, plots=self.plots)

        with open("report.html",'w') as f:
            f.writelines(html)