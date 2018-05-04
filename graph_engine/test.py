from common.figure import Figure
from graphEngine import Engine

fig_1 = Figure(0, 1.0, 1.0, "or", "red", "rectangle", "big") #
fig_2 = Figure(1, 4.0, 0.0, "or", "red", "triangle", "small") 
fig_3 = Figure(2, 4.0, 3.0, "or", "green", "triangle", "medium") #
fig_4 = Figure(3, 3.0, 2.0, "or", "blue", "circle", "big") #
fig_5 = Figure(4, 2.0, 2.0, "or", "green", "circle", "medium") # 
fig_6 = Figure(5, 1.0, 3.0, "or", "blue", "rectangle", "big") #
fig_7 = Figure(6, 1.0, 5.0, "or", "red", "triangle", "small")
fig_8 = Figure(7, 5.0, 3.0, "or", "green", "circle", "big") #
fig_9 = Figure(8, 0.0, 2.0, "or", "blue", "triangle", "small") #
fig_10 = Figure(9, 2.0, 1.0, "or", "blue", "triangle", "small") #

figures = [fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7, fig_8, fig_9, fig_10]

engine = Engine()
engine.add_figures(figures)

