import numpy as np
from bokeh.models import ColumnDataSource, CustomJS, TapTool, HoverTool
from bokeh.plotting import figure, output_file, show
import os

output_file("scatter_sound_example.html")


x = np.random.rand(10)
y = np.random.rand(10)


file_list = os.listdir('/home/ianwonilkim/wav2vec/one_shot_percussive_sounds')
audio_files=[]
for s_name in file_list:
    local_path= 'http://localhost:8000/one_shot_percussive_sounds/'+ s_name
    audio_files.append(local_path)



source = ColumnDataSource(dict(
    x=x,
    y=y,
    audio_files=audio_files
))

plot = figure(width=400, height=400, tools="tap,wheel_zoom,pan", title="Scatter Plot")
plot.circle("x", "y", source=source, size=10)

# Hover Tool
hover = HoverTool(tooltips=[("X", "@x"), ("Y", "@y"), ("Audio", "@audio_files")])
plot.add_tools(hover)


callback = CustomJS(args=dict(source=source), code="""
    var selected_index = source.selected.indices[0];
    if (selected_index !== undefined) {
        var data = source.data;
        var audio_file = data['audio_files'][selected_index];
        var audio = new Audio();
        audio.src = audio_file;
        audio.play();
    }
""")

taptool = plot.select(type=TapTool)
taptool.callback = callback

show(plot)
