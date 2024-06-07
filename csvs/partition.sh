# Extract the header row
head -n 1 Partida.csv > header.csv

# Split the file into parts without the header row
split -l $(( $(wc -l < Partida.csv) / 10 + 1 )) Partida.csv part_

# Add the header row to each split file and rename them
partition_number=1
for i in part_*; do
    cat header.csv "$i" > temp && mv temp "$i"
    original_name="Partida.csv"
    new_name="${partition_number}_Part_${original_name%.csv}.csv"
    mv "$i" "$new_name"
    ((partition_number++))
done

# Remove the temporary header file
rm header.csv
