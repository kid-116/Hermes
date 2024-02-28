[![Lint](https://github.com/kid-116/Hermes/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/kid-116/Hermes/actions/workflows/lint.yml)

# Hermes

## Getting Started

### Setup

#### Linux
1. Setup python virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r ./requirements.txt
    ```
2. Save Firebase private key to `root/credentials.json`.
3. Setup secrets.
    ```bash
    cp .stremlit/secrets.toml.sample .streamlit/secrets.toml
    ```
    Now, fill in the secrets.

### Running the App
```bash
streamlit run app.py
```

### Development

#### Formatting
1. To get suggested formatting changes:
    ```bash
    yapf -d -r .
    ```
2. To apply the suggested changes in place:
    ```bash
    yapf -i -r .
    ```

#### Linting
```bash
pylint --recursive=y .
```

#### Type Checking
```bash
mypy .
```

## Dataset
- [MIMIC Clinical Database Demo](https://physionet.org/content/mimic-iv-demo/2.2/)

## Reference Papers
- [Data Quality Considerations for Big Data and Machine Learning: Going Beyond Data Cleaning and Transformations](https://personales.upv.es/thinkmind/dl/journals/soft/soft_v10_n12_2017/soft_v10_n12_2017_1.pdf)

  Gudivada, Venkat & Apon, Amy & Ding, Junhua. (2017). Data Quality Considerations for Big Data and Machine Learning: Going Beyond Data Cleaning and Transformations. International Journal on Advances in Software. 10. 1-20.

- [Assessing Data Quality: An Approach and an Application](https://bseim.web.unc.edu/wp-content/uploads/sites/9932/2021/05/A-Measurement-Assessment-Approach-PA_May2021.pdf)

  McMann K, Pemstein D, Seim B, Teorell J, Lindberg S. Assessing Data Quality: An Approach and An Application. Political Analysis. 2022;30(3):426-449. doi:10.1017/pan.2021.27

- [Developing a Systematic Approach to Assessing Data Quality in Secondary Use of Clinical Data Based on Intended Use](https://onlinelibrary.wiley.com/doi/epdf/10.1002/lrh2.10264)

  Razzaghi H, Greenberg J, Bailey LC. Developing a systematic approach to assessing data quality in secondary use of clinical data based on intended use. Learn Health Sys. 2022; 6:e10264. https://doi.org/10.1002/lrh2.10264

- [Discovering Data Quality Problems](https://aisel.aisnet.org/bise/vol61/iss5/3/#:~:text=Existing%20methodologies%20for%20identifying%20dataquality,structures%20and%20data%20governance%20frameworks.)

  Zhang, Ruojing; Sadiq, Shazia; and Indulska, Marta (2019) "Discovering Data Quality Problems," Business & Information Systems Engineering: Vol. 61: Iss. 5, 575-593. Available at: https://aisel.aisnet.org/bise/vol61/iss5/3

- [Data Quality Assessment for Improved Decision-Making: A Methodology for Small and Medium-Sized Enterprises](https://www.sciencedirect.com/science/article/pii/S2351978919301477)

  Lisa C. Günther, Eduardo Colangelo, Hans-Hermann Wiendahl, Christian Bauer, Data quality assessment for improved decision-making: a methodology for small and medium-sized enterprises, https://doi.org/10.1016/j.promfg.2019.02.114.

- [A Survey of Data Quality Measurement and Monitoring Tools](https://www.frontiersin.org/articles/10.3389/fdata.2022.850611/full)

  Ehrlinger L and Wöß W (2022) A Survey of Data Quality Measurement and Monitoring Tools. Front. Big Data 5:850611. doi: 10.3389/fdata.2022.850611

## Links
- [Drive](https://drive.google.com/drive/folders/1nZDxrEn82BJPJAxpljf-AHgAEe_o2oN1?usp=drive_link)
- [Notes](https://docs.google.com/document/d/1oj72QnhO1ppDBaduS_ihxjQ79RPnggzIXx-01UaVW9U)
- [Diagrams](https://drive.google.com/file/d/1fIjxpNIov2ClquNP6MjMdr43eJKfwyck/view?usp=sharing)
- [Report](https://docs.google.com/document/d/1qsBM0EbIVAkBEcIhTpDmR49D0lkKsCyxxLnF7T8ZDHg/edit?usp=sharing)
