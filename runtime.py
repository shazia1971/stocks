from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
from warnings import simplefilter
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

simplefilter(action='ignore', category=FutureWarning)

app = FastAPI()
# request only accepted from the local host
# Set up CORS middleware if needed
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Add other origins if necessary
]
# checks the validity of the request before implementing through server
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define the SmaCross strategy
class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

class Trade(BaseModel):
    symbol: str
    strategy: str
    commission: float
    exclusive_orders: bool
    cash: float = 10000

@app.put("/", summary="Backtesting API", response_class=HTMLResponse, description="GOOGLE Stock Trading Strategy using SMA Cross for 4 Year Period with Specified Commission")
async def home(trade: Trade = Trade(symbol="GOOG", strategy="SmaCross", commission=.002, exclusive_orders=True, cash=10000)):
    try:
        # ignore the following code this generates our fancy HTML plot file for the stock trading
        bt = Backtest(GOOG, SmaCross, commission=trade.commission, exclusive_orders=trade.exclusive_orders, cash=trade.cash, trade_on_close=True)
        stats = bt.run()
        plot_path = os.path.join("templates", "SmaCross_plot.html")
        bt.plot(filename=plot_path, open_browser=False)
        # this is going to return the HTML file with the plot
        with open('templates/SmaCross_plot.html') as f:
            plot = f.read()
        return HTMLResponse(content=plot, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/trade_summary', summary="Trade Summary", response_class=HTMLResponse, description="Trade Summary for the Backtesting API on GOOGLE Stock Trading Strategy using SMA Cross for 4 Year Period with Specified Commission")
async def trade_summary(trade: Trade = Trade(symbol="GOOG", strategy="SmaCross", commission=.002, exclusive_orders=True, cash=10000)):
    try:
        # ignore the following code this generates our fancy HTML plot file for the stock trading
        bt = Backtest(GOOG, SmaCross, commission=trade.commission, exclusive_orders=trade.exclusive_orders, cash=trade.cash, trade_on_close=True)
        stats = bt.run()
        
        return PlainTextResponse(content=str(stats), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
