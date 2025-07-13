#!/bin/bash

benchmark="--benchmark"
output_dir="benchmarks"

function print_usage() {
	echo -e "\nUsage: $0 [-o output_dir] [-a] [-m mode]"
	echo -e "\tUse -a to run the full benchmark suite.\n\tOtherwise, just the default tests are run"
}

while [[ "${1}" != "" ]]; do
	case "${1}" in
		-a)
			benchmark="--benchmark --benchmark-all"
			;;
		-o) 
			output_dir="$2"
			shift 1
			;;
		-m)
			mode="-m $2"
			shift 1
			;;
		*)
			print_usage
			exit 1
			;;
	esac
	shift 1
done

if [[ -e "${output_dir}/benchmark_1.txt" ]]; then
	echo -e "\nWARNING: Output directory \"${output_dir}\" already exists!"
	echo -e "You can define a new directory with -o \"new_directory\"."
	echo -e "Do you wish to continue and overwrite it?\n"
	printf "Y/[N]: "
	read answer
	
	if [[ "${answer}" = "Y" || "${answer}" = "y" ]]; then
		true
	else
		exit 0
	fi
fi

if [[ ! -d "${output_dir}" ]]; then
	mkdir -p "${output_dir}"
fi

start_time="$(date '+%F %T')"

for i in {1..5}; do
	echo -e "\n\t###############"
	echo -e "\t# Benchmark $i #"
	echo -e "\t###############\n"
	date '+%F %T'
	echo

	outfile="${output_dir}/benchmark_$i"

	hashcat ${benchmark} ${mode} --machine-readable | tee "${outfile}.txt"
	./parser.py "${outfile}.txt" "${outfile}.json"
done

end_time="$(date '+%F %T')"

echo -e "\n###################################"
echo -e "# Start time: ${start_time} #\n# End time: ${end_time}   #"
echo -e "###################################\n"

echo "Merging hashcat benchmarks..."
./merger.py -o "$output_dir/merged.json" "${output_dir}"/benchmark_{1..5}.json
echo -e "\nTo compare results use\n./comparator.py [-o outfile.json] benchmark_a/merged.json benchmark_b/merged.json\n"
