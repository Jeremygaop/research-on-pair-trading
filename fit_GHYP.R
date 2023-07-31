library(ghyp)

spread = read.csv("/Users/shezihua/Downloads/DBF-2610/spread.csv")

X = spread$X0
rm(spread)

ar1 = arima(X, order=c(1, 0, 0))

Box.test(ar1$residuals, lag=12, type="Ljung")

pv=1-pchisq(68768, 11)
pv

resi = ar1$residuals

hist(resi)

fit.ghypuv(resi)  # may not converge

pacf(resi, 10)
acf(X, 10)
pacf(X, 10)
