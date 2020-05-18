# Add CMS-1500 backgrounds to Intergy output

The medical billing software [Intergy] prints out the data needed to
fill CMS-1500 forms -- but assumes they will be physically printed
onto physical CMS-1500 forms.  It is often useful to be able to skip
this physical step, however, and [Intergy] provides no way to include
the empty form itself in the output.

This builds a OS X application which [Intergy] PDFs can be dragged onto;
it will rewrite the PDF to also contain the empty form behind the raw data
provided in the PDF.


# Setup

```
python3 -m venv virtualenv
source ./virtualenv/bin/activate
pip install -r requirements.txt
```

# Building new versions

- Update `VERSION` in `setup.py`
- Update `CHANGELOG.md`
- Run `./build.sh`
- Distribute `dist/Add CMS1500 to Intergy.dmg`


# Limitations

 - All errors are output to STDOUT, which is never seen by the user.
   Options to address this include bundling tkinter or wxPython, or
   shelling out to Applescript to create pop-ups.

 - It is quite fragile to the shape of the input.  It errs on the side
   of doing nothing rather than touching a file it doesn't recognize.

 - It's an unsigned OS X application, which means that additional
   steps are required to run it.


[Intergy]: https://www.greenwayhealth.com/intergy
