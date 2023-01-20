import requests
import pandas as pd


def getSession() -> requests.session:
    headers = {
        "authority": "opstra.definedge.com",
        "origin": "https://opstra.definedge.com",
        "referer": "https://opstra.definedge.com/results-calendar",
        "user-agent": requests.get(
            "https://techfanetechnologies.github.io"
            + "/latest-user-agent/user_agents.json"
        ).json()[-2],
        "accept": "application/json, text/plain, */*",
        "cookie": "JSESSIONID=F9A9F1839BA0533842E387C1AA0A94DA",
    }
    session = requests.session()
    session.get(
        "https://opstra.definedge.com", headers={"user-agent": headers["user-agent"]}
    )
    session.headers.update(headers)
    return session


if __name__ == "__main__":
    s = getSession()

    resultsCalender = s.get("https://opstra.definedge.com/api/resultscalendar").json()

    pd.DataFrame.from_records(resultsCalender).to_csv(
        "HistoricalResultCalender.csv", index=False
    )

    s.headers.update(
        {"referer": "https://opstra.definedge.com/historical-results-timings"}
    )

    tickers = s.get("https://opstra.definedge.com/api/tickers").json()

    for ticker in tickers[3:]:
        print(ticker)
        if ticker != "SHRIRAMFIN":
            df = pd.DataFrame.from_records(
                s.get(
                    f"https://opstra.definedge.com/api/resultscalendar/{ticker}"
                ).json()
            )
            df.drop(columns="Symbol", inplace=True)
            df.to_csv(f"{ticker}-HistoricalResultCalender.csv", index=False)
