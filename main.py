import streamlit as st
from front.pageone import pageconfig, pageone


def main():
    # Configuração da página
    pageconfig()

    # Exibir a primeira página
    pageone()           
    
if __name__ == "__main__":
    main()
    st.caption ('Copyright 2024, Cristian Ferreira Carlos, Todos os direitos reservados.' )
    st.caption ('https://www.linkedin.com/in/cristian-ferreira-carlos-256b19161/')
