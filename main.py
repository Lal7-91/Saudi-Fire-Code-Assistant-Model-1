from functions import *
import streamlit as st
from streamlit_option_menu import option_menu



def main():
    
    SBCC = "SBCC801.pdf"
    st.title("SFCA")



    def chois_menu():
            
            chois = option_menu(
                menu_title=None,  
                options=["English"," ", "عربي"],  
                icons=["list","home","list"],    
                default_index= 1,  
                orientation="horizontal",
            )
            
            return chois
        
    chois = chois_menu()
    
    if chois == " ": 
        
        st.write("## Welcome to Saudi Fire Code Assistant")
        st.write("### Please choose your language")


        st.write("## مرحبا بك في مساعدة اللوائح السعودية للحريق")
        st.write("### الرجاء اختيار اللغة")
        st.divider()
        st.write("### Made by: Saleh Ahmed")
        st.write("### X: LAl7_91")




    
    elif chois == "English":        
        
    
        
        question = st.text_input(
            "Ask qustion about this topic",
            placeholder= ("Ask ")
        )

        if question:
            
            text = load_and_extract_one_pdf("SBCC801.pdf")

            with st.spinner("Just a sec .."):
                
                response = ask(SBCC, question)
                
                st.write("## Answer")
                st.write(response)

    elif chois == "عربي":        
        
        
        question = st.text_input(
            "اطرح سؤالك حول هذا الموضوع",
            placeholder= ("اطرح سؤالك")
        )

        if question:
            
            text = load_and_extract_one_pdf("SBCC801.pdf")

            with st.spinner("انتظر قليلا .."):
                
                response = ask(SBCC, question)
                
                st.write("## الاجابة")
                st.write(response)


if __name__ == "__main__":
    main()