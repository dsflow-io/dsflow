FROM python:3.6-slim

RUN pip install numpy scipy pandas matplotlib pyarrow

# https://plot.ly/dash/installation
RUN pip install dash==0.19.0  # The core dash backend
RUN pip install dash-renderer==0.11.1  # The dash front-end
RUN pip install dash-html-components==0.8.0  # HTML components
RUN pip install dash-core-components==0.14.0  # Supercharged components
RUN pip install plotly --upgrade  # Plotly graphing library used in examples
RUN pip install dash_table_experiments

WORKDIR /home/dash/

COPY ./dash .
# EXPOSE 8050

CMD ["python", "app.py"]
