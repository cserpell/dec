# coding=utf-8
"""Load substation lists and write files with csv format."""
import json

FILE1 = 'substation_locs/sub_sig_20181016234836.json'
FILE2 = 'substation_locs/sub_sing_20181016234836.json'


def one_record(feat):
    """Get one output line."""
    one = feat['properties']
    geo = feat['geometry']
    return ','.join([
        one['nombre'],
        one['propiedad'],
        one['tension_kv'],
        one['tipo'],
        one['f_operacio'],
        one['rca'],
        one['sist_elect'],
        one['estado'],
        one['coord_este'],
        one['coord_nort'],
        one['huso'],
        one['datum'],
        one['region'],
        one['provincia'],
        one['comuna'],
        one['fuente_bas'],
        one['fech_crea'],
        one['fech_act'],
        str(geo['coordinates'][0]),
        str(geo['coordinates'][1]),
    ])


def main():
    """Main run point."""
    with open(FILE1) as file1:
        loaded1 = json.load(file1)
    with open(FILE2) as file2:
        loaded2 = json.load(file2)
    with open('outputfile.csv', 'w') as outfile:
        outfile.write(','.join([
            'nombre',
            'propiedad',
            'tension_kv',
            'tipo',
            'f_operacio',
            'rca',
            'sist_elect',
            'estado',
            'coord_este',
            'coord_nort',
            'huso',
            'datum',
            'region',
            'provincia',
            'comuna',
            'fuente_bas',
            'fech_crea',
            'fech_act',
            'coordinates_1',
            'coordinates_2',
        ]))
        for feat in loaded1['features']:
            outfile.write(one_record(feat))
            outfile.write('\n')
        for feat in loaded2['features']:
            outfile.write(one_record(feat))
            outfile.write('\n')


if __name__ == '__main__':
    main()
