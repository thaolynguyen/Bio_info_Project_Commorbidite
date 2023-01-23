import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Standard Imports
import io
import requests# Third-Party Imports
import pandas as pd
import streamlit as st





# Data analyze

# Read CSV, drop column and rename column
df = pd.read_csv('comorbidites.csv', delimiter = ';',encoding="utf8")
df = df.drop(['region', 'dept', 'comorbidite', 'annee', 'top'], axis =1)
df.rename(columns = {'ncomorb':'Nb patient commorbidity'}, inplace = True)
df.rename(columns = {'ntop':'Nb patient pathology'}, inplace = True)
df.rename(columns = {'proportion_comorb':'comorb/patho'}, inplace = True)

# Filter diseases

df_cancer = df[df.patho_niv1 =='Cancers']
df_diabete =  df[df.patho_niv1 =='Diabète']
df_psy = df[df.patho_niv1 =='Maladies psychiatriques']
df_defmental= df_psy[df_psy.patho_niv2 =='Déficience mentale']
df_trouble_addictif =  df_psy[df_psy.patho_niv2 =='Troubles addictifs']





# Functions definition

def extract_commorb_cancer(cancer, nb):
    df = df_cancer[df_cancer.patho_niv2 == cancer]
    df = df.sort_values(by = 'Nb patient commorbidity', ascending = False).head(nb)
    col_list = ['libelle_comorbidite', 'comorb/patho']
    list_comor = df[col_list]
    return list_comor

def top_commor(df, nb):
    comor = df.sort_values(by = 'Nb patient commorbidity', ascending = False).head(nb)
    col_list = ['libelle_comorbidite', 'comorb/patho']
    comor = comor[col_list]
    return comor

def filter_commor(df, del_list):
    df = df.drop(del_list)
    return df

def compare_2_lists(l1,l2):  
    nb = 0
    for i in l1:
        if i in l2:
            nb = nb+1
    return nb

def get_common(d1,d2):
    temp = []
    for i in d1:
        if i in d2:
            temp.append(i)
    return temp
    


# ------------------------------------------------------------------------------------------ CANCER

cancer_comor = df_cancer.sort_values(by = 'Nb patient commorbidity', ascending = False).head(20)
col_list = ['libelle_comorbidite', 'comorb/patho']
cancer_comor = cancer_comor[col_list]

list_del = [17679, 25086,23633,14605,11691,11693,5954,1521,9168,15016,20679,19211,22172,1535,37,4438]
cancer_comor = cancer_comor.drop(list_del)


cancer_colocteral_comor = extract_commorb_cancer('Cancer colorectal',30)
cancer_prostate_comor = extract_commorb_cancer('Cancer de la prostate', 30)
cancer_poumon_comor = extract_commorb_cancer('Cancer du poumon', 30)
cancer_sein_comor = extract_commorb_cancer('Cancer du sein de la femme', 30)

cancer_prostate_comor = cancer_prostate_comor.loc[[9065,9067,9135,4548,3095,9135]]
cancer_poumon_comor = cancer_poumon_comor.loc[[9175,4606,9177,20859,4607]]
cancer_colocteral_comor = cancer_colocteral_comor.loc[[11847,8941,12240,3043,19271]]
cancer_sein_comor =  cancer_sein_comor.loc[[12548,17932,3205,4665]]

# ------------------------------------------------------------------------------------------ DIABETE

diabete_comor = top_commor(df_diabete,30)
list_del_2 = [12309,6255,23918,9780,17989,12672,15217,23919,347,23920,17990,25367,22464,19516,3273,12311,15219,12674,23921,6256,25368,7772,348,17991,15628]
diabete_comor = filter_commor(diabete_comor, list_del_2)

# ---------------------------------------------------------------------------------- MALADIES PSYCHIATRIQUES
psy_comor = top_commor(df_psy,30)
list_del_3= [10913,16727,24706,11346,4042,5530,16729,5531,23248,8567,8568,1118,11348,17186,14354,16881,14354,16881,21832,8642,18786,1197,4123,20319,8569,7061,17316]
psy_comor = filter_commor(psy_comor, list_del_3)

# Mental deficiency
defmental_comor = top_commor(df_defmental,30)
list_del_4= [1148,17256,16803,14282,1149,21794,7095,4080,13929,21795,7096,26193,24745,1150,4081]
defmental_comor = filter_commor(defmental_comor, list_del_4)

# Addictive disorder
addict_comor = top_commor(df_trouble_addictif,30)


# ------------------------ LABEL

# Label
label_diabete = diabete_comor['libelle_comorbidite'].tolist()
value_diabete = diabete_comor['comorb/patho'].tolist()
value_diabete  = np.round(value_diabete,2)

label_psy = psy_comor['libelle_comorbidite'].tolist()
value_psy = psy_comor['comorb/patho'].tolist()
value_psy  = np.round(value_psy,2)

label_cancer = cancer_comor['libelle_comorbidite'].tolist()
value_cancer = cancer_comor['comorb/patho'].tolist()
value_cancer  = np.round(value_cancer,2)



st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/ASSURANCE_MALADIE.svg/2560px-ASSURANCE_MALADIE.svg.png", width=500)
st.title('Comorbidities associated with each pathology')



# Using "with" notation
with st.sidebar:
    st.image("https://www.efrei.fr/wp-content/uploads/2022/01/LOGO_EFREI-PRINT_EFREI-WEB.png")
    st.title('About the data')
    st.write("The data present information on co-morbidities associated with conditions (or chronic treatments or episodes of care) identified by the Caisse Nationale de l'Assurance Maladie (Cnam): among the patients managed for a given condition (or chronic treatment or episode of care), some may also be managed for one or more other conditions, called co-morbidities.")
    st.write("Link of dataset : https://www.data.gouv.fr/fr/datasets/comorbidites-associees-a-chaque-pathologie/")
    st.caption("Presented by Florence NGUYEN M2 DAI EFREI Paris, Bio Informatic course ")



tab1, tab2, tab3 = st.tabs(["Explanation", "Diseases & commorbidities", "Commorbidities similarity"])



with tab1:
    st.header("General explanation")
    st.title('What is commorbidity ?')
    st.write("A comorbidity is any coexisting health condition. The prefix “co” means together and the word “morbidity” is the medical term for a health condition. It can also be described as cooccurring or coexisting conditions.Comorbidities sometimes interact with each other, but they can also exist entirely separately. Some conditions may raise your risk of developing others, or may commonly occur together. For example, a heart attack often occurs with stroke or vascular disease. Chronic kidney disease may occur with hypertension and anemia.Comorbidities are often chronic conditions and can include physical or mental health. possible to have many comorbidities at the same time. For example, a person could have depression, arthritis, diabetes, and high blood pressure. ")
    st.caption('Source : https://www.healthline.com/health/comorbidity#definition')
    
    st.write("Pathologies, chronic treatments and episodes of care are grouped into the following categories. Patient numbers are also presented in the data. The reference population is that of the Health Insurance mapping of pathologies and expenditures.")
    st.markdown("- cardio-neurovascular diseases" )
    st.markdown("- vascular risk treatments (excluding cardiovascular pathologies)")
    st.markdown("- diabetes")
    st.markdown("- cancers")
    st.markdown("- psychiatric disease")
    st.markdown("- psychotropic treatments (excluding psychiatric pathologies)")
    st.markdown("- neurological and degenerative diseases")
    st.markdown("- chronic respiratory diseases")
    st.markdown("- inflammatory or rare diseases or human immunodeficiency virus (HIV) or AIDS")
    st.markdown("- chronic end-stage renal failure (CTRF)")
    st.markdown("- liver or pancreas diseases")
    st.markdown("- other long-term illnesses (ALD including 31 and 32)")
    st.markdown("- full hospitalization stays for Covid-19 management (from 2020)")
    st.markdown("- maternity")
    st.markdown("- chronic treatment with analgesics, non-steroidal anti-inflammatory drugs (NSAIDs) and corticosteroids")
    st.markdown("- one-time hospital stays")


with tab2:
    st.header("Diseases & commorbidities")
    pathology= st.selectbox(
    "Select the pathology",
    ("Cancer", "Diabete", "Psychiatric disease"))

    if pathology == "Psychiatric disease":
        st.header("Psychiatric diseases")
        col1, col2 = st.columns(2)
        with col1:
            st.image('https://pacifichealthsystems.com/wp-content/uploads/2021/03/mental-health-1281-600x385.jpg', width = 300)
        with col2:
            st.caption("Psychiatry is the branch of medicine that focuses on mental, emotional, and behavioral disorders.  As such, the term, “psychiatric disorder,” refers to a broad range of problems that disturb a person’s thoughts, feelings, behavior or mood. Also referred to as “mental illness,” and “mental health conditions,” psychiatric disorders can significantly affect a person’s ability to perform at work or school, or maintain healthy social relationships. Important note: Mental illness is not a weakness. It is a medical condition. Psychiatric disorders are treatable, though the most effective treatments vary from person to person, depending on the specific disorder and the scope and severity of the symptoms.")
        


        st.header("Top 4 commobidities and percentage")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label=label_psy[0], value = value_psy[0])
        with col2:
            st.metric(label=label_psy[1],value = value_psy[1])
        with col3:
            st.metric(label=label_psy[2], value = value_psy[2])
        with col4:
            st.metric(label=label_psy[3], value = value_psy[3])

     
        

        psy_type= st.selectbox(
        "Select psychatric disease",
        ("Mental deficiency", "Addictive disorder"))

        if psy_type == "Mental deficiency":
            st.dataframe(defmental_comor)
        if psy_type == "Addictive disorder":
            st.dataframe(addict_comor)






    if pathology == "Diabete":
        st.header("Diabete")
        col1, col2 = st.columns(2)
        with col1:
            st.image('https://mydiabetesmyway.scot.nhs.uk/media/3253/whats_going_on_in_my_body_t2_v3.jpg', width = 300)
        with col2:
            st.caption("With diabetes, your body either doesn't make enough insulin or can't use it as well as it should. Diabetes is a chronic (long-lasting) health condition that affects how your body turns food into energy. Your body breaks down most of the food you eat into sugar (glucose) and releases it into your bloodstream.")



        st.header("Top 4 commobidities and percentage")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label=label_diabete[0], value = value_diabete[0])
        with col2:
            st.metric(label=label_diabete[1],value = value_diabete[1])
        with col3:
            st.metric(label=label_diabete[2], value = value_diabete[2])
        with col4:
            st.metric(label=label_diabete[3], value = value_diabete[3])


    if pathology == 'Cancer':
        st.header("Cancer")
        col1, col2 = st.columns(2)
        with col1:
            st.image('https://www.cancercouncil.com.au/wp-content/uploads/2021/01/How-cancer-starts-500px.png', width = 300)
        with col2:
            st.caption("Cancer is a disease caused when cells divide uncontrollably and spread into surrounding tissues. Cancer is caused by changes to DNA. Most cancer-causing DNA changes occur in sections of DNA called genes. These changes are also called genetic changes. For all types of cancer, here are the main commorbidities we can find")
        
       
        st.header("Top 4 commobidities and percentage")

    
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label=label_cancer[0], value = value_cancer[0])
        with col2:
            st.metric(label=label_cancer[1],value = value_cancer[1])
        with col3:
            st.metric(label=label_cancer[2], value = value_cancer[2])
        with col4:
            st.metric(label=label_cancer[3], value = value_cancer[3])

        cancer_type= st.selectbox(
        "Select the cancer type",
        ("Lungs", "Prostate", "Breast", "Colocteral"))

        if cancer_type == "Colocteral":
            st.dataframe(cancer_colocteral_comor)
        elif cancer_type == "Breast":
            st.dataframe(cancer_sein_comor)
        elif cancer_type == "Prostate":
            st.dataframe(cancer_prostate_comor)
        else:
            st.write(cancer_poumon_comor)

        st.header("Comparison")


        compare = st.multiselect(
        'Select cancer',
        ["Lungs", "Prostate", "Breast", "Colocteral"])



        if "Lungs" in compare:
            st.caption("Lungs cancer")
            st.dataframe(cancer_poumon_comor)
        if "Breast" in compare:
            st.caption("Breast cancer")
            st.dataframe(cancer_sein_comor)
        if "Prostate" in compare:
            st.caption("Prostate cancer")
            st.dataframe(cancer_prostate_comor)
        if "Colocteral" in compare:
            st.caption("Colocteral cancer")
            st.dataframe(cancer_colocteral_comor)

with tab3:
    st.header("Diseases similarities")
    st.write("Two diseases can have one or several commorbidities in common. Here you can compare which disease can be close to another in function of their commorbidities. The first disease you select is the reference and the other disease is the one you want to compare with.")
    d1= st.selectbox(
    "Select the first disease",
    ("Cancer", "Diabete", "Psychiatric disease"))

    d2= st.selectbox(
    "Select the second disease",
    ("Cancer", "Diabete", "Psychiatric disease"))

    if d1 and d2 != "":
            if d1 == "Cancer":
                l1 = label_cancer
            if d1 == "Diabete":
                l1 =label_diabete
            if d1 == "Psychiatric disease":
                l1 = label_psy

            if d2 == "Cancer":
                l2 = label_cancer
            if d2 == "Diabete":
                l2 =label_diabete
            if d2 == "Psychiatric disease":
                l2 = label_psy

        



            common = compare_2_lists(l1,l2)
            l_common = get_common(l1,l2)

            st.write("👉 Number of commorbidities in common : ", common)
            st.write("👉 Common  / Total commorbidities of first disease : ",(common/len(d1)*100))
            st.write("👉 List of common commorbidities : ", l_common)
    







   






    




