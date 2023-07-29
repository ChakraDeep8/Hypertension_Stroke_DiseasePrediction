import time
import streamlit as st
import pandas as pd
from Classifier_Models import Classifier_model_builder_kidney as cmb
import pickle
import numpy as np


def app():
    st.title("Kidney Disease Detector")
    st.info("This app predicts whether a person have any kidney disease or not")

    st.sidebar.header('User Input Features')
    # st.sidebar.markdown("""
    # [Import input CSV file](https://github.com/ChakraDeep8/Heart-Disease-Detector/tree/master/res)""")

    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
    else:
        def patient_details():
            age = st.sidebar.slider('Age', 2, 90)
            bp = st.sidebar.slider('Blood Pressure', 50, 180)
            sg = st.sidebar.slider('Salmonella Gallinarum - SG', 1.00, 1.02, step=0.01)
            al = st.sidebar.slider('Albumin', 0, 5)
            su = st.sidebar.slider('Sugar - SU', 0, 5)
            bgr = st.sidebar.slider('Blood Glucose Regulator - BGR', 22, 490)
            bu = st.sidebar.slider('Blood Urea - BU', 2, 90)
            sc = st.sidebar.slider('Serum Creatinine - SC', 1.5, 391.0, step=0.1)
            sod = st.sidebar.slider('Sodium', 45, 163)
            pot = st.sidebar.slider('Potassium', 2.5, 47.0, step=0.1)
            hemo = st.sidebar.slider('Hemoglobin', 3.1, 17.8, step=0.1)
            pcv = st.sidebar.slider('Packed Cell Volume - PCV', 9, 54)
            wc = st.sidebar.slider('White Blood Cell Count - WC', 3800, 26400)
            rc = st.sidebar.slider('Red Blood Cell Count - RC', 4, 80)
            rbc = st.sidebar.selectbox('Red Blood Corpulence', ('normal', 'abnormal'))
            pc = st.sidebar.selectbox('Post Cibum - PC', ('normal', 'abnormal'))
            pcc = st.sidebar.selectbox('Prothrombin Complex Concentrates - PCC', ('present', 'notpresent'))
            ba = st.sidebar.selectbox('Bronchial Asthma - BA', ('present', 'notpresent'))
            htn = st.sidebar.selectbox('Hypertension - HTN', ('yes', 'no'))
            dm = st.sidebar.selectbox('Diabetes Mellitus', ('yes', 'no'))
            cad = st.sidebar.selectbox('Coronary Artery Disease - CAD', ('yes', 'no'))
            appet = st.sidebar.selectbox('Appetite', ('poor', 'good'))
            pe = st.sidebar.selectbox('Pulmonary Embolism - PE', ('yes', 'no'))
            ane = st.sidebar.selectbox('Acute Necrotizing Encephalopathy - ANE', ('yes', 'no'))

            data = {'age': age,
                    'rbc': rbc,
                    'pc': pc,
                    'pcc': pcc,
                    'bp': bp,
                    'ba': ba,
                    'htn': htn,
                    'dm': dm,
                    'cad': cad,
                    'appet': appet,
                    'pe': pe,
                    'ane': ane,
                    'sg': sg,
                    'al': al,
                    'su': su,
                    'bgr': bgr,
                    'bu': bu,
                    'sc': sc,
                    'sod': sod,
                    'pot': pot,
                    'hemo': hemo,
                    'pcv': pcv,
                    'wc': wc,
                    'rc': rc,
                    }

            features = pd.DataFrame(data, index=[0])
            return features

        input_df = patient_details()

    url = "res/dataset/kidney.csv"
    kidney_disease_raw = pd.read_csv(url)
    kidney_disease_raw = kidney_disease_raw.loc[:, ~kidney_disease_raw.columns.str.contains('^Unnamed')]
    kidney = kidney_disease_raw.drop(columns=['target'])
    df = pd.concat([input_df, kidney], axis=0)

    # Encoding of ordinal features
    encode = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']
    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummy], axis=1)
        del df[col]
    df = df[:1]  # Selects only the first row (the user input data)
    df.loc[:, ~df.columns.duplicated()]

    if uploaded_file is not None:
        st.write(df)
    else:
        st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
        df = df.loc[:, ~df.columns.duplicated()]
        st.write(df)

    # Load the classification models
    load_clf_NB = pickle.load(open('res/pickle/kidney_disease_classifier_NB.pkl', 'rb'))
    load_clf_KNN = pickle.load(open('res/pickle/kidney_disease_classifier_KNN.pkl', 'rb'))
    load_clf_DT = pickle.load(open('res/pickle/kidney_disease_classifier_DT.pkl', 'rb'))
    load_clf_LR = pickle.load(open('res/pickle/kidney_disease_classifier_LR.pkl', 'rb'))
    load_clf_RF = pickle.load(open('res/pickle/kidney_disease_classifier_RF.pkl', 'rb'))

    # Apply models to make predictions
    prediction_NB = load_clf_NB.predict(df)
    prediction_proba_NB = load_clf_NB.predict_proba(df)
    prediction_KNN = load_clf_KNN.predict(df)
    prediction_proba_KNN = load_clf_KNN.predict_proba(df)
    prediction_DT = load_clf_DT.predict(df)
    prediction_proba_DT = load_clf_DT.predict_proba(df)
    prediction_LR = load_clf_LR.predict(df)
    prediction_proba_LR = load_clf_LR.predict_proba(df)
    prediction_RF = load_clf_RF.predict(df)
    prediction_proba_RF = load_clf_RF.predict_proba(df)

    def NB():
        st.subheader('Naive Bayes Prediction')
        NB_prediction = np.array([0, 1])
        if NB_prediction[prediction_NB] == 1:
            st.write("<p style='font-size:20px;color: orange'><b>You have kidney disease.</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Naive Bayes Prediction Probability')
        st.write(prediction_proba_NB)
        cmb.plt_NB()

    def KNN():
        st.subheader('K-Nearest Neighbour Prediction')
        knn_prediction = np.array([0, 1])
        if knn_prediction[prediction_KNN] == 1:
            st.write("<p style='font-size:20px;color: orange'><b>You have kidney disease.</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('KNN Prediction Probability')
        st.write(prediction_proba_KNN)
        cmb.plt_KNN()

    def DT():
        st.subheader('Decision Tree Prediction')
        DT_prediction = np.array([0, 1])
        if DT_prediction[prediction_DT] == 1:
            st.write("<p style='font-size:20px; color: orange'><b>You have kidney disease.</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Decision Tree Prediction Probability')
        st.write(prediction_proba_DT)
        cmb.plt_DT()

    def LR():
        st.subheader('Logistic Regression Prediction')
        LR_prediction = np.array([0, 1])
        if LR_prediction[prediction_LR] == 1:
            st.write("<p style='font-size:20px; color: orange'><b>You have kidney disease.<b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Logistic Regression Probability')
        st.write(prediction_proba_LR)
        cmb.plt_LR()

    def RF():
        st.subheader('Random Forest Prediction')
        RF_prediction = np.array([0, 1])
        if RF_prediction[prediction_RF] == 1:
            st.write("<p style='font-size:20px; color: orange'><b>You have kidney disease.</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Random Forest Probability')
        st.write(prediction_proba_RF)
        cmb.plt_RF()

    def predict_best_algorithm():
        if cmb.best_model == 'Naive Bayes':
            NB()

        elif cmb.best_model == 'K-Nearest Neighbors (KNN)':
            KNN()

        elif cmb.best_model == 'Decision Tree':
            DT()

        elif cmb.best_model == 'Logistic Regression':
            LR()

        elif cmb.best_model == 'Random Forest':
            RF()
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)

    # Displays the user input features
    with st.expander("Prediction Results"):
        # Display the input dataframe
        st.write("Your input values are shown below:")
        st.dataframe(input_df)
        # Call the predict_best_algorithm() function
        st.caption('Here, The best algorithm is selected among all algorithm')
        predict_best_algorithm()

    # Create a multiselect for all the plot options
    selected_plots = st.multiselect("Select plots to display",
                                    ["Naive Bayes", "K-Nearest Neighbors", "Decision Tree", "Logistic Regression",
                                     "Random Forest"])

    # Check the selected plots and call the corresponding plot functions

    placeholder = st.empty()

    # Check the selected plots and call the corresponding plot functions
    if "Naive Bayes" in selected_plots:
        with st.spinner("Generating Naive Bayes...."):
            cmb.plt_NB()
            time.sleep(1)

    if "K-Nearest Neighbors" in selected_plots:
        with st.spinner("Generating KNN...."):
            cmb.plt_KNN()
            time.sleep(1)

    if "Decision Tree" in selected_plots:
        with st.spinner("Generating Decision Tree...."):
            cmb.plt_DT()
            time.sleep(1)

    if "Logistic Regression" in selected_plots:
        with st.spinner("Generating Logistic Regression...."):
            cmb.plt_LR()
            time.sleep(1)

    if "Random Forest" in selected_plots:
        with st.spinner("Generating Random Forest...."):
            cmb.plt_RF()
            time.sleep(1)

    # Remove the placeholder to display the list options
    placeholder.empty()