import streamlit as st

def display_contact_info():
    """
    Display the contact information of developers.
    """

    # Include FontAwesome CDN in your app
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

    # Developer Contacts
    with st.container(border=True):
        st.header("Developer Contacts", divider=True)
        
        with st.container(border=True):
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(
                    '<i class="fas fa-user"></i> Harris Lukundi<br>'
                    '[Email](mailto:harris.lukundi@student.moringaschool.com)<br>'
                    '[Github](https://github.com/AtomHarris)',
                    unsafe_allow_html=True
                )
            with col2:
                st.write("Developers Profile")
                st.write(" ...")
        with st.container(border=True):    
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(
                    '<i class="fas fa-user"></i> Brian Muthama<br>'
                    '[Email](mailto:brian.muthama@student.moringaschool.com)<br>'
                    '[Github](https://github.com/Muthama42)',
                    unsafe_allow_html=True
                )
            with col2:
                st.write("Developers Profile")
                st.write(" ...")
        with st.container(border=True):
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(
                    '<i class="fas fa-user"></i> Beryl Agai<br>'
                    '[Email](mailto:beryl.agai@student.moringaschool.com)<br>'
                    '[Github](https://github.com/Agai-Beryl)',
                    unsafe_allow_html=True
                )
            with col2:
                st.write("Developers Profile")
                st.write(" ...")
        with st.container(border=True):
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(
                    '<i class="fas fa-user"></i> Chris Laaria<br>'
                    '[Email](mailto:laaria.chris@student.moringaschool.com)<br>'
                    '[Github](https://github.com/laaria-chris)',
                    unsafe_allow_html=True
                )
            with col2:
                st.write("Developers Profile")
                st.write(" ...")
        with st.container(border=True):
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(
                    '<i class="fas fa-user"></i> Henry Rono<br>'
                    '[Email](mailto:henry.rono@student.moringaschool.com)<br>'
                    '[Github](https://github.com/RonoHenry)',
                    unsafe_allow_html=True
                )
            with col2:
                st.write("Developers Profile")
                st.write(" ...")
        with st.container(border=True):
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown(
                    '<i class="fas fa-user"></i> Lynette Wangari<br>'
                    '[Email](mailto:lynette.wangari@student.moringaschool.com)<br>'
                    '[Github](https://github.com/Wangari-web)',
                    unsafe_allow_html=True
                )
            with col2:
                st.write("Developers Profile")
                st.write(" ...")




def contact_form():
    """Display the contact form and handle form submissions."""
    with st.container(border=True):
        st.header("Contact Us", divider=True)
        st.write("Please fill out the form below to send us a message.")
        
        # Create placeholders for form fields
        name_placeholder = st.empty()
        email_placeholder = st.empty()
        subject_placeholder = st.empty()
        message_placeholder = st.empty()

        with st.form(key='contact_form'):
            # Use placeholders to hold the form fields
            name = name_placeholder.text_input("Name")
            email = email_placeholder.text_input("Email")
            subject = subject_placeholder.text_input("Subject")
            message = message_placeholder.text_area("Message")
            
            submit_button = st.form_submit_button("Send")
            
            if submit_button:
                if name and email and subject and message:
                    # Call your function to send an email
                    # send_email(name, email, subject, message)
                    
                    # Show success message
                    st.success("Your message has been sent successfully!")
                    
                    # Clear form fields using placeholders
                    name_placeholder.text_input("Name", value="", key="name")
                    email_placeholder.text_input("Email", value="", key="email")
                    subject_placeholder.text_input("Subject", value="", key="subject")
                    message_placeholder.text_area("Message", value="", key="message")
                else:
                    st.error("Please fill out all fields.")


