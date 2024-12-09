"""Flask App (/update for taking data u(t), updating the simulation, /plot for data to plot)"""
from flask import Flask, requests, jsonify 
from modules.simulation import calculate_heat_loss_glass, calculate_heat_loss_walls, calculate_next_temperature
import requests as request

app = Flask(__name__)

