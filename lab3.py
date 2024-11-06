#This for env file
AI_SERVICE_ENDPOINT='https://xxxxxxxxxxxx.cognitiveservices.azure.com/'
AI_SERVICE_KEY='xxxxxxxxZAgoECf3RJh8xg2c49nS2gtNv880fNNANceVtWvzHmeWJQQJ99AKACYeBjFXJ3w3AAAAACOGc8qL'
#This code for read text image 
from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def main():
    global cv_client
    try:
        # Load configuration settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        
        # Authenticate Azure AI Vision client
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )
        
        # Menu for text reading functions
        print('\n1: Use Read API for image (Lincoln.jpg)\n2: Read handwriting (Note.jpg)\nAny other key to quit\n')
        command = input('Enter a number: ')
        
        if command == '1':
            image_file = os.path.join('images', 'Lincoln.jpg')
            GetTextRead(image_file)
        elif command == '2':
            image_file = os.path.join('images', 'Note.jpg')
            GetTextRead(image_file)
    
    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('\n')
    
    # Open image file
    with open(image_file, "rb") as f:
        image_data = f.read()
    
    # Use Analyze image function to read text in image
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )
    
    # Display the image and overlay it with the extracted text
    if result.read is not None:
        print("\nText:")
        
        # Prepare image for drawing
        image = Image.open(image_file)
        fig = plt.figure(figsize=(image.width / 100, image.height / 100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'
        
        for line in result.read.blocks[0].lines:
            # Print detected text
            print(f"  {line.text}")
            
            drawLinePolygon = True
            r = line.bounding_polygon
            bounding_polygon = ((r[0].x, r[0].y), (r[1].x, r[1].y), (r[2].x, r[2].y), (r[3].x, r[3].y))
            
            # Print bounding polygon
            print("   Bounding Polygon: {}".format(bounding_polygon))
            
            # Print each word and draw bounding polygon
            for word in line.words:
                r = word.bounding_polygon
                bounding_polygon = ((r[0].x, r[0].y), (r[1].x, r[1].y), (r[2].x, r[2].y), (r[3].x, r[3].y))
                print(f"    Word: '{word.text}', Bounding Polygon: {bounding_polygon}, Confidence: {word.confidence:.4f}")
                
                drawLinePolygon = False
                draw.polygon(bounding_polygon, outline=color, width=3)
            
            # Draw line bounding polygon if no word polygons were drawn
            if drawLinePolygon:
                draw.polygon(bounding_polygon, outline=color, width=3)
        
        # Display and save the image with results
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'text.jpg'
        fig.savefig(outputfile)
        print('\n  Results saved in', outputfile)

if name == "main":
    main()
