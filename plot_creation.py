####
# plot_creation.py
# 
# Functions will be in charge of creating plots using matplotlib
# and then converting them into html string so that they can be 
# posted onto the webpages as images
###
import pandas as pd
import matplotlib
import matplotlib.figure as figure
import base64
from io import BytesIO

# Function creates html string given a figure.Figure() object
# @para fig:
# @return: html string that will be used to load the image
#          this string can be inserted in src for html script. Ex:
#         <img src='HTML_STRING'/>
def create_html_string(fig):
  html_string = ""
  
  buf = BytesIO()
  fig.savefig(buf, format="png")
  
  # Embed the result in the html output
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  html_string = f'data:image/png;base64,{data}'
  
  return html_string



# Creates scatter plot that compares x and y axis parameters
# @para     x: array of x-axis values
# @para   x_l: string of x-axis value
# @para     y: array of y-axis values
# @para   y_l: string of y-axis value
# @para title: string title of plot
# @return: html string that will load the image (refer to create_html_string()
#          function for more details)
def create_scatter_html(x, x_l, y, y_l, title):
    fig = figure.Figure()
    scatter = fig.add_subplot()
    scatter.scatter(x=x, y=y)
    scatter.set_xlabel(x_l)
    scatter.set_ylabel(y_l)
    scatter.set_title(title)
    
    # Create and return html string
    
    return create_html_string(fig)
  
  
# Creates barchart that compares given x paramaters, graphs output
# their heights based on height instance
# @para        x: array of x-axis values
# @para      x_l: string of x-axis value
# @para   height: array of heights for given x values
# @para height_l: string of label for heights
# @para    title: string title of plot
# @return: html string that will load the image (refer to create_html_string()
#          function for more details)
def create_bar_html(x, x_l, height, height_l, title):
    fig = figure.Figure()
    bar = fig.add_subplot()
    bar.bar(x=x, height=height)
    bar.set_xlabel(x_l)
    bar.set_ylabel(height_l)
    bar.set_title(title)
    
    # Create and return html string
    return create_html_string(fig)