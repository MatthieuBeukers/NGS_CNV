import os
import sys
import argparse

# Import classes
from classes.arraycnv import ArrayCnv

# Import generate_totals scripts
import generate_totals.array_cnvs as gtac
import generate_totals.classifications as gtcf
import generate_totals.total_calls as gttc

# Import parameter script
import parameters.parameters as parpar

# Import util scripts
import utils.filereaders as ufr
import utils.filewriters as ufw


TOOL_CHOICES = ["arraycnv", "classification", "numofcalls", "numofna"]
REQUIRED_PARAMS = {"arraycnv": ["arrayfile", "infile", "outfile", "outprefix"],
                   "classification": ["infile", "outfile"],
                   "numofcalls": ["infile"],
                   "numofna": ["infile"]}
OPTIONAL_PARAMS = {}
PARAM_TYPES = {"infile": "inputfile",
               "arrayfile": "inputfile",
               "outfile": "outputfile",
               "outprefix": "string"}
TOOL_USAGE = {"arraycnv": "python totals.py -t arraycnv -i cnv_classifications.txt -a arraycnvdata.txt",
              "classification": "python totals.py -t classification -i cnv_classifications.txt -o /path/to/outdir -op prefixname",
              "numofcalls": "python totals.py -t numofcalls -i cnv_classifications.txt",
              "numofna": "python totals.py -t numofna -i cnv_classifications.txt"}


def main():
    totalsparams = parpar.get_totals_params(TOOL_CHOICES)
    if parpar.parameters_are_ok(totalsparams, REQUIRED_PARAMS, PARAM_TYPES):
        # Determine the total number of array CNVs found and missed
        if totalsparams["tool"] == "arraycnv":
            outpath = totalsparams["outfile"] + "/" + totalsparams["outprefix"]
            arraydata = ufr.read_array_cnvs(totalsparams["arrayfile"])

            found_arraycnvs = gtac.determine_arraycnvs_found(totalsparams["infile"], arraydata)
            found_summary = gtac.summarize_arraycnv_types(found_arraycnvs)
            missed_arraycnvs = gtac.determine_arraycnvs_missed(found_arraycnvs, arraydata)
            missed_summary = gtac.summarize_arraycnv_types(missed_summary)

            ufw.write_missedfound_arraycnvs(found_arraycnvs, f"{outpath}_found_arraycnvs.txt")
            ufw.write_missedfound_summary(found_summary, f"{outpath}_found_arraycnvs_summary.txt")
            ufw.write_missedfound_arraycnvs(missed_arraycnvs, f"{outpath}_missed_arraycnvs.txt")
            ufw.write_missedfound_summary(missed_summary, f"{outpath}_missed_arraycnvs_summary.txt")

        # Gather the totals per classification label
        if totalsparams["tool"] == "classification":
            gatkresults = ufr.read_classification_file(tg_params["infile"])
            totalsdata = gtcf.generate_classification_totals(gatkresults)
            filewritten = ufw.write_classification_totals(totalsdata, tg_params["outfile"])
            print(f"Wrote outfile?: {filewritten}")

        # Gather the total number of GATK4 Calls
        if totalsparams["tool"] == "numofcalls":
            gttc.get_total_calls(totalsparams["infile"])

        # Gather the total number of GATK4 calls that overlap with an array CNV
        if totalsparams["tool"] == "numofna":
            gttc.get_total_calls(totalsparams["infile"], True)


if __name__ == "__main__":
    main()
