import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from GA import GeneticAlgorithm
from otsu import my_otsu

def convert_to_grayscale(image_path, output_path):
    """Convert an image to grayscale and return the grayscale image."""
    try:
        with Image.open(image_path) as img:
            grayscale_image = img.convert('L')
            grayscale_image.save(output_path)
        return grayscale_image
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    
def apply_threshold(t, image, output_path):
    """Apply the threshold to the image and save the result."""
    image_array = np.asarray(image)
    thresholded_array = np.where(image_array < t, 0, 255).astype(np.uint8)
    thresholded_image = Image.fromarray(thresholded_array)
    thresholded_image.save('image/output.jpg')


def plot_thresholds(thresholds, N, max_iterations):
    """Plot the thresholds over iterations."""
    plt.figure()
    plt.title(f"Thresholds (N={N}, iterations={max_iterations})", fontsize=12)
    plt.plot(thresholds, linewidth=1)
    plt.xlabel('Iteration')
    plt.ylabel('Threshold')
    plt.show()

 
def plot_fitness(fitness_values, N, max_iterations):
    """Plot the fitness values over iterations."""
    plt.figure()
    plt.title(f"Fitness (N={N}, iterations={max_iterations})", fontsize=12)
    plt.plot(fitness_values, linewidth=1)
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.show()


def main():
    """Main function to perform genetic algorithm-based thresholding on an image."""
    try:
        image_path = 'image/meng.jpg'
        grayscale_image_path = 'image/meng_gray.jpg'
        output_image_path = 'image/output.jpg'

        im_gray = convert_to_grayscale(image_path, grayscale_image_path)
        if im_gray is None:
            return
    
        population_size = 8
        max_iterations = 100
        ga = GeneticAlgorithm(im_gray, population_size, max_iterations)

        
        best_threshold, thresholds, fitness_values, cur_iteration = ga.get_threshold()

      
        apply_threshold(best_threshold, im_gray, output_image_path)

     
        plot_thresholds(thresholds, population_size, max_iterations)
        plot_fitness(fitness_values, population_size, max_iterations)

    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
