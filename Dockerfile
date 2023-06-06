FROM manimcommunity/manim:v0.16.0.post0

USER root

# Create a new user 'navigator' and set the password
RUN useradd --create-home --shell /bin/bash navigator \
    && echo 'navigator:navigator' | chpasswd \
    && usermod -aG sudo navigator && pip install --no-cache-dir georinex

# Copy the Navigation directory to the user's home directory
# Navigation is the directory containig all the python code 
COPY Navigation/ /home/navigator/

RUN chown -R navigator:navigator /home/navigator 

# Set the working directory for the 'navigator' user
WORKDIR /home/navigator/Nav

# Switch to the 'navigator' user
USER navigator

# Set the entrypoint to a bash shell and display user, password, and name
ENTRYPOINT ["/bin/bash", "-c", "echo 'User: navigator, Password: navigator' && exec /bin/bash"]
