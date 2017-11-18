FROM python:3-alpine

RUN pip install dash==0.17.7 && \
  pip install dash-renderer==0.7.4 && \
  pip install dash-html-components==0.7.0 && \
  pip install dash-core-components==0.12.0 && \
  pip install plotly==2.0.13  # Plotly graphing

COPY . .
EXPOSE 8050

CMD ["python", "app.py"]
