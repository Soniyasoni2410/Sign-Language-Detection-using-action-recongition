# Sign Language Detection Using Action Recognition

## Overview
A real-time Sign Language Detection system leveraging action recognition. Uses computer vision and machine learning to identify and translate sign language gestures into text or audio output, enhancing accessibility in communication.

## Features
- **Real-Time Detection**: Detects and translates sign gestures via webcam or uploaded videos/images.
- **User-Friendly Interface**: Tkinter GUI for intuitive interaction.
- **Text and Audio Output**: Provides output in both text and audio forms.
- **Learning Module**: Includes preloaded videos for specific gestures, helping users learn sign language.

## Technologies Used
- **Frontend**: Tkinter (Python GUI toolkit)
- **Backend**: Python with:
  - **MediaPipe**: Hand tracking and landmark detection
  - **scikit-learn**: Gesture classification with Random Forest
  - **OpenCV**: Video processing
  - **NumPy**: Numerical operations
- **Data**: Preloaded dataset of sign language images for model training

## Project Structure
- **Sign Detection Module**: Uses MediaPipe for hand detection and extracts features for classification.
- **Training Module**: Random Forest classifier trained on sign gestures.
- **Learning Module**: Preloaded video tutorials for each sign.
- **GUI Interface**: Tkinter-based interface for an easy-to-use experience.

## Methodology
1. **Data Collection**: Compile images and videos of sign gestures.
2. **Hand Landmark Detection**: MediaPipe detects hand landmarks.
3. **Feature Extraction**: Extracts coordinates from hand landmarks.
4. **Gesture Classification**: Classifies gestures using Random Forest.
5. **Output Generation**: Converts gestures to text or audio.
6. **User Training Module**: Tutorials with videos for specific signs.

## Usage
- **Run the Program**: Start the main application.
- **Detection**: Choose live webcam detection.
- **Output Options**:View results in text.
- **Learning Module**: Select words for video tutorials on gesture.
  
## Future Enhancements
- Expand sign language support to include additional signs and languages.
- Improve model accuracy with more advanced ML algorithms.
- Add user customization for audio output.


##  Acknowledgments
  Thanks to the creators of MediaPipe, OpenCV, and scikit-learn for their powerful tools that made this project possible.
  
This includes a well-structured **Future Enhancements** section, as well as the overall project information. Let me know if you’d like more customization or changes!
