"""
This program looks for a certain microorganism species that the user inputs,
into any number of csvs in the working directory (that have the suffix "final_reads.csv")
and extracts the number of reads that this species is associated with.
Then it creates a bar chart that showcases the differences in those reads,
between each different file.

Biology background:
This program has been created as part of a larger analysis of human gut microbiota datasets.
Each working csv contains the microbiota species present in fecal samples of humans from different backgrounds.
Those csvs are the end products of Whole Genome or Amplicon sequencing analysis.
The number of reads indicates the number of times that species has appeared in the sample.

CSV origins:
The csvs used for this analysis were the resulting product of a previous analysis,
hence their "final_results" suffix, that is mentioned.
The csvs used at the first step of the pipeline were downloaded
from the MG-RAST database (https://www.mg-rast.org/), hence the mgIDs mentioned later.

CSV form eligible for analysis with this program:
The csvs that can potentially be analyzed by this program and yield similar end results
and visualizations, as per its original purpose, should meet some certain criteria.
1. They have a column named species (name subjugated to change) that contains the microbiota species
2. They have a column named reads (name subjugated to change) that contains the number of reads for each species.

"""


# import libraries
import csv
import glob
import matplotlib.pyplot as plt
import pandas as pd
import os


def choose_species():
    """
    This function asks the user for a bacteria species input.
    It returns the given input as a variable.
    NOTE: The species must be written exactly as it appears in the csv file.
    """
    print("")
    print("Enter a bacteria species. Please be mindful of syntax.")
    print("(Best practise to copy + paste the name directly from the csv)")
    search_species = input("Enter species here: ")
    print("")

    return search_species


def shorten_name(f):
    """
    This function takes as input a file and 
    returns a shorter version of its name (as a string variable),
    that contains the dataset's name and mgID that correspond to this file.
    """
    # store the file's name in variable
    filename = f.name
    # split the filename in a list
    # index[0] contains the dataset's name and its mgID
    split_filename = filename.split("_final_results.csv")
    # extract index[0] from the split_filename list into a variable
    short_filename = split_filename[0]

    return short_filename


def create_species_dict(csv_list, search_species):
    """
    This function creates a list of dictionaries.
    Each dictionary contains two keys (filename, reads)
    and two corresponding values (shortened name of the file, number of reads).
    input: csv_list, the species the user searched for
    returns: the list of dictionaries
    """
    # create empty list that will later contain the species dictionaries
    results_list = []

    # loop through the csv list
    for csv_file in csv_list:
        # loop through each file separately
        with open(csv_file) as f:
            # give back each line as a dictionary
            # keys: Species, Pathway, Reads
            reader = csv.DictReader(f)

            # returns the part of the filename that contains the dataset's name and mgID
            short_filename = shorten_name(f)

            # variable indicator of the number of times the program has seen the searched species in a file
            species_counter = 0

            for line in reader:
                # if the line that's read contains the searched bacteria species
                if line["Species"] == search_species:
                    # species_counter goes up by 1
                    species_counter += 1

                    # create empty dictionary, which will later store the valid results of the search
                    search_results = {}
                    # add to search_results dict -> key: str(filename), value: short_filename
                    search_results["filename"] = short_filename
                    # add to search_results dict -> key: str(reads), value: Reads from original csv file
                    search_results["reads"] = line["Reads"]

                    # add in result_list the created search_results dictionary
                    results_list.append(search_results)
            
            # If after the check of every line of the file the species_counter is still 0
            # then that means that the program hasn't encountered the species the user searches for
            if species_counter == 0:
                # create empty dictionary, which will later store the valid results of the search
                search_results = {}
                # add to search_results dict -> key: str(filename), value: short_filename
                search_results["filename"] = short_filename
                # add to search_results dict -> key: str(reads), value: 0
                search_results["reads"] = 0

                # add in result_list the created search_results dictionary
                results_list.append(search_results)

    print(results_list)

    return results_list


def results_to_csv(search_species, results_list):
    """
    This function exports as a csv the list of dictionaries that contain information 
    about each filename and the number of reads associated with the microorganism in question.
    input: the searched species, the list of dictionaries
    returns: a csv named after the microorganism, that contains information about its appearance in every file
    """
    # place the searched species in a new variable (for easier documentation inside the function)
    csv_filename = search_species
    # create list that will hold the names of the new csv columns
    csv_columns = ["filename", "reads"]

    # create csv file with the species name and loop through it
    with open(csv_filename + ".csv", "w") as csv_export:
        # maps each dictionary into a csv row and places the items of csv_columns list as headers
        writer = csv.DictWriter(csv_export, fieldnames = csv_columns)
        # looks for the list passed as fieldnames and makes its components headers
        writer.writeheader()
        # writes the values of each dictionary as a line in the new csv
        writer.writerows(results_list)


def create_bar_chart(working_dir, search_species):
    """
    This function creates a bar chart, that showcases the number of reads, by each file,
    corresponding to the searched microorganism species.
    title: the name of the microorganism species
    x axis: filename
    y axis: number of reads for that microorganism species

    input: working dir, searched species
    returns: the created bar chart
    """
    # get the filepath of the created microorganism csv
    results_csv_filepath = working_dir + "\\" + search_species + ".csv"
    # read the microorganism csv and store it in a variable
    results_csv = pd.read_csv(results_csv_filepath)
    # create a data frame from the data of the microorganism csv
    df = pd.DataFrame(results_csv)

    # create a variable that will store the new figure and specify the figure's size
    bar_chart = plt.figure(figsize=(8, 6))

    # set X (x axis) values as the different filenames inside the microorganism csv
    X = list(df.filename)
    # set Y (y axis) values as the different reads inside the microorganism csv
    Y = list(df.reads)
    # plot the data using bar() method
    plt.bar(X, Y, color='maroon', width=0.1)  # width = width of the columns
    plt.title(str(search_species))
    plt.xlabel("Datasets")
    plt.ylabel("Num of reads")

    # show the bar chart
    plt.show()

    return bar_chart


def main():
    # ask the user to choose a working directory
    working_dir = input("Please choose the working directory: ")

    # change current directory to the chosen working directory
    os.chdir(working_dir)

    # put csvs (with the suffix "final_results) of the working directory in a list
    csv_list = glob.glob("*final_results.csv")
    print(csv_list)

    # ask user for microorganism input
    search_species = choose_species()

    # create list of dictionaries which contain the filenames and the number of reads associated with the microorganism
    # keys: filename, reads
    # values: short_filename, number of reads from original csv
    results_list = create_species_dict(csv_list, search_species) 

    # export list of dictionaries to csv
    results_to_csv(search_species, results_list)

    # visualize the differences in reads between each file as a bar chart
    bar_chart = create_bar_chart(working_dir, search_species)

    # save the bar chart as a png named after the searched species
    bar_chart.savefig(search_species + ".png")


if __name__ == '__main__':
    main()
