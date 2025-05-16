import streamlit as st
from front.pageone import pageconfig, pageone


def main():
    # Configuração da página
    pageconfig()

    # Exibir a primeira página
    pageone()           
    
if __name__ == "__main__":
    main()
