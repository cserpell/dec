# coding=utf-8
"""Script to group by substation and hour load demand files."""
import argparse
import logging
import os

import numpy as np
import pandas as pd

import dates_util

# Constants with column names to avoid programming errors
SIC_HORA_MENSUAL = 'Hora_Mensual'
SIC_MEDIDAHORARIA2 = 'MedidaHoraria2'
SIC_NOMBRE_BARRA = 'nombre_barra'
SIC_TIPO1 = 'tipo1'
SING_FECHAMEDIDA = 'fechaMedida'
SING_IDNODOMEDIDA = 'idNodoMedida'
SING_IDNODOREF = 'idNodoRef'
SING_IDTIPOMEDIDA = 'idTipoMedida'
SING_IDTRAMO = 'idTramo'
SING_IDUSOMEDIDA = 'idUsoMedida'
SING_ISINYECCION = 'isInyeccion'
SING_PERIODOMEDIDA = 'periodoMedida'
SING_VALORKWH = 'valorkWh'
OUTPUT_NODE = 'node_id'
OUTPUT_VALUE = 'value'

SING_NODES = {
    'ABLANCAS13': 'AG.BLANCAS____013',
    'AGUILA66': 'AGUILA________066',
    'AHOSPICIO110': 'A.HOSPICIO____110',
    'AHOSPICIO13': 'A.HOSPICIO____013',
    'ALTON110': 'ALTONORTE_____110',
    'ANDES220': 'ANDES_SNG_____220',
    'ANDES345': 'ANDES_SNG_____345',
    'ANGAMOS220': 'ANGAMOS_______220',
    'ANTOFA110': 'ANTOFAGASTA___110',
    'ANTOFA13': 'ANTOFAGASTA___013',
    'ANTUCOYA220': 'ANTUCOYA______220',
    'ARICA110': '',  # Moved to MENORES_ARICA
    'ARICA13': 'ARICA_________013',
    'ARICA66': 'ARICA_________066',
    'ARRIERO220': 'ARRIERO_______220',
    'ATACAM220': 'ATACAMA_______220',
    'BARRIL220': 'BARRILES_____220',
    'BOMBEO_2': '',
    'BOMBEO_3': '',
    'BOMBEO_4': '',
    'CALAMA110': 'CALAMA________110',
    'CALAMA220': 'CALAMA________220',
    'CALAMA220_2': 'CALAMA________220',
    'CAPRI110': 'CAPRICORNIO___110',
    'CAPRI13': '',
    'CAPRI220': 'CAPRICORNIO___220',
    'CDARICA13': 'CD.ARICA______013',
    'CDARICA66': 'CD.ARICA______066',
    'CDRAGON110': 'C.DRAGON______110',
    'CDIQUIQ13': 'CD.IQUIQUE____013',
    'CDIQUIQ66': 'CD.IQUIQUE____066',
    'CDRAGON13': 'C.DRAGON______013',
    'CDTAMA110': 'CD.TAMAYA_____110',
    'CENTRO110': 'CENTRO________110',
    'CHACA110': 'CHACAYA_______110',
    'CHACA220': 'CHACAYA_______220',
    'CHANGOS220': 'L.CHANGOS_____220',
    'CHANGOS500': 'L.CHANGOS_____500',
    'CHUQUI110': 'CHUQUICAMATA__100',
    'CHUQUI220': 'CHUQUICAMATA__220',
    'COLLA220': 'COLLAHUASI____220',
    'CONCHI220': 'CONCHI________220',
    'CONDOR220': 'CONDORES______220',
    'CRUCER220': 'CRUCERO_______220',
    'CTM ARRANQUE': '',
    'CUMBRES500': 'CUMBRES_______500',
    'C_DOMIN220': 'C.DOMINADOR___220',
    'DESAL110': 'DESALANT______110',
    'DOLOR110': 'TOFF.DOLORES__110',
    'DOLOR23': 'TOFF.DOLORES__023',
    'DOMEY220': 'DOMEYKO_______220',
    'ELABRA220': 'ELABRA________220',
    'ELABRA220_2': '',
    'ELABRA220_3': '',
    'ELCOBRE220': 'ELCOBRE_______220',
    'ENCUEN220': 'ENCUENTRO_____220',
    'ENCUEN220_2': '',
    'ESCOND220': 'ESCONDIDA_____220',
    'ESMERA110': 'ESMERALDA_____110',
    'ESMERA220': 'ESMERALDA_____220',
    'ESPERANZA220': 'ESPERANZA_SNG_220',
    'INACESA23': 'INACESA_______023',
    'IQUIQ13': 'IQUIQUE_______013',
    'IQUIQ66': 'IQUIQUE_______066',
    'KAPATUR220': 'KAPATUR_______220',
    'KM6': 'KM6___________100',
    'LABERINTO220': 'LABERINTO_____220',
    'LACRUZ220': 'LACRUZ________220',
    'LAGUNA220': 'LAGUNAS_______220',
    'LAGUNA220_2': '',
    'LAGUNA23': 'LAGUNAS_______023',
    'LLANOS220': '',
    'LOA220': 'LOA___________220',
    'MARIA_ELENA220': 'M.ELENA_______220',
    'MBLANC220': 'M.BLANCOS_____220',
    'MBLANC23': 'M.BLANCOS_____023',
    'MEJI110': 'MEJILLONES____110',
    'MEJI220': 'MEJILLONES____220',
    'MEJI23': 'MEJILLONES____023',
    'MENORES_ARICA': 'ARICA_________110',  # Changed from ARICA110
    'MIRAJE220': 'MIRAJE________220',
    'NEGRA110': 'NEGRA_________110',
    'NEGRA23': 'NEGRA_________023',
    'NEGRO110': 'EL_NEGRO______110',
    'NVACARDO220': 'N.CARDONES____220',
    'NVACARDO500': 'N.CARDONES____500',
    'NVAVIC220': 'N.VICTORIA____220',
    'NVAZAL220': 'N.ZALDIVAR____220',
    'OESTE220': 'OESTE_________220',
    'OHIGG220': 'OHIGGINS______220',
    'PARINA220': 'PARINACOTA____220',
    'PEQ220': 'PEQ___________220',
    'POLPAICO23': '',  # This is a SIC substation 'POLPAICO______023'
    'PORTA23': 'LAPORTADA_____023',
    'POZO110': 'P.ALMONTE_____110',
    'POZO110_C': '',
    'POZO13': 'P.ALMONTE_____013',
    'POZO13_1': '',
    'POZO23': 'P.ALMONTE_____023',
    'POZO220': 'P.ALMONTE_____220',
    'POZO66': 'P.ALMONTE_____066',
    'RTOMIC220': 'R.TOMIC_______220',
    'S_GORDA220': 'S.GORDA_______220',
    'SALAR110': 'SALAR_________110',
    'SALAR220': 'SALAR_________220',
    'SULFU220': 'SULFUROS______220',
    'SUR110': 'SUR___________110',
    'TAMAR66': 'TAMARUGAL_____066',
    'TAPOFFQUIANI66': 'TOFF.QUIANI___066',
    'TARAP11': '',
    'TARAP220': 'TARAPACA______220',
    'TESORO220': 'TESORO________220',
    'TOCO5': 'TOCOPILLA_____005',
    'TOCO110': 'TOCOPILLA_____110',
    'TOCO220': 'TOCOPILLA_____220',
    'URIBE110': 'URIBE_________110',
    'ZALDIV220': 'ZALDIVAR______220',
}


class Script:
    """Script to group data by substation from all files in a directory."""

    def __init__(self, directory):
        """Constructor of Script."""
        self._directory = directory  # Directory where args file is located
        self._sing_bars = list(SING_NODES.keys())
        self._sing_consider_bars = [
            key for key, value in SING_NODES.items() if value != '']
        self._sing_mock_tramos = self.build_mock_tramos()
        self._sing_mock_tramo_ref = ['MBLANC220 - MBLANC23',
                                     'MINERA M. BLANCOS']

    def build_mock_tramos(self):
        """Build a list of tramos to not consider when reading SING files."""
        mock_tramos = {'{} - {}'.format(b1, b2): True
                       for b1 in self._sing_bars
                       for b2 in self._sing_bars}
        mock_tramos.update({'{} - {} 1'.format(b1, b2): True
                            for b1 in self._sing_bars
                            for b2 in self._sing_bars})
        mock_tramos.update({'{} - {} 2'.format(b1, b2): True
                            for b1 in self._sing_bars
                            for b2 in self._sing_bars})
        mock_tramos.update({'TAPOFF{} - {}'.format(b1, b2): True
                            for b1 in self._sing_bars
                            for b2 in self._sing_bars})
        mock_tramos.update({'{} - TAPOFF{}'.format(b1, b2): True
                            for b1 in self._sing_bars
                            for b2 in self._sing_bars})
        mock_tramos.update({'TAPOFF{} - TAPOFF{}'.format(b1, b2): True
                            for b1 in self._sing_bars
                            for b2 in self._sing_bars})
        del mock_tramos['AGUILA66 - ARICA66']
        del mock_tramos['LAGUNA220 - LAGUNA23']
        del mock_tramos['NVAZAL220 - ESCOND220']
        del mock_tramos['NVAZAL220 - SULFU220']
        del mock_tramos['OHIGG220 - TAPOFFBOMBEO_2']
        del mock_tramos['MBLANC220 - MBLANC23']
        del mock_tramos['SALAR220 - SALAR110']
        del mock_tramos['TARAP220 - TARAP11']
        del mock_tramos['ZALDIV220 - ESCOND220']
        mock_tramos['AHOSPICIO110 - TAPOFFAHOSP110'] = True
        mock_tramos['ANDES220 - ANDESSOLAR'] = True
        mock_tramos['ANDES220 - BESSANDES'] = True
        mock_tramos['ARICA110 - ARICA110PM66'] = True
        mock_tramos['ARICA13 - ARICA13 SSAA'] = True
        mock_tramos['ARICA66 - ARICA110PM66'] = True
        mock_tramos['ARRIERO220 - ARRIERO33'] = True
        mock_tramos['ATACAM220 - TAPOFFENLACE220'] = True
        mock_tramos['ATACAM220 - TG1A'] = True
        mock_tramos['ATACAM220 - TG2A'] = True
        mock_tramos['ATACAM220 - TG1B'] = True
        mock_tramos['ATACAM220 - TG2B'] = True
        mock_tramos['BARRIL220 - BARRIL110'] = True
        mock_tramos['C_DOMIN220 - S_GORDA220'] = True
        mock_tramos['CAPRI220 - CAPRI220PM110'] = True
        mock_tramos['CALAMA220 - SOLAR_JAMA'] = True
        mock_tramos['CONCHI220 - CERROPABELLON'] = True
        mock_tramos['C_DOMIN220 - C_DOMIN FV'] = True
        mock_tramos['KAPATUR220 - KAPATUR SSAA'] = True
        mock_tramos['IQUIQ13 - CDNEPSA13'] = True
        mock_tramos['IQUIQ13 - IQUIQUE13 SSAA'] = True
        mock_tramos['KAPATUR220 - KELAR220 1'] = True
        mock_tramos['KAPATUR220 - KELAR220 2'] = True
        mock_tramos['LABER220 - MBLANC220'] = True
        mock_tramos['MELENA220 - TAPOFFQUILLA220'] = True
        mock_tramos['MENORES_ARICA - CHIZA'] = True
        mock_tramos['MENORES_ARICA - MAL_PASO'] = True
        mock_tramos['MENORES_ARICA - VITOR'] = True
        mock_tramos['POZO110 - POZO220PM110_1'] = True
        mock_tramos['POZO110 - POZO110PM66'] = True
        mock_tramos['POZO13 - POZO110PM66'] = True
        mock_tramos['POZO13-PAS2'] = True
        mock_tramos['POZO13-PAS3'] = True
        mock_tramos['POZO66 - POZO110PM66'] = True
        mock_tramos['TAMAR66 - LOS PUQUIOS'] = True
        mock_tramos['TAPOFFSIERRA220 - ARRIERO220'] = True
        mock_tramos['TARAP220 - TARAP13'] = True
        mock_tramos['TOCO5 - AES_GENER SSAA'] = True
        return mock_tramos

    def run(self):
        """Perform script actions."""
        all_arrays = []
        for file_obj in os.scandir(self._directory):
            if file_obj.is_file() and file_obj.path.endswith('.csv'):
                new_array = self.process_csv_file(file_obj.path)
                if new_array is not None:
                    all_arrays.append(new_array)
            else:
                logging.info('Ignoring file %s', file_obj.path)
        # Using same variable name to remove all arrays from memory
        all_arrays = pd.concat(all_arrays, axis=0)
        logging.info('Writing all data rows file')
        all_arrays.to_csv(
            path_or_buf=os.path.join(self._directory, 'all_data_rows.csv'),
            index=False)
        # TODO: Add sanity check that there is only one row per node / date
        column_names = [first for first, _ in dates_util.COLUMNS]
        logging.info('Writing total data file')
        total_value = all_arrays.pivot_table(
            index=column_names, values=[OUTPUT_VALUE],
            aggfunc=np.sum).reset_index()
        total_value.to_csv(
            path_or_buf=os.path.join(self._directory, 'total_data.csv'),
            index=False)
        logging.info('Writing all data columns file')
        the_array = all_arrays.pivot_table(
            index=column_names, values=[OUTPUT_VALUE], columns=[OUTPUT_NODE],
            aggfunc=np.sum).reset_index()
        the_array.columns = [one if two == '' else two
                             for one, two in the_array.columns]
        the_array.to_csv(
            path_or_buf=os.path.join(self._directory, 'all_data_columns.csv'),
            index=False)

    @staticmethod
    def load_csv(file_name):
        """Reads the content of a csv file."""
        try:
            the_array = pd.read_csv(file_name, sep=',', header=0)
        except UnicodeDecodeError:
            the_array = pd.read_csv(file_name, sep=',', header=0,
                                    encoding='ISO-8859-1')
        return the_array

    @staticmethod
    def process_sic_file(file_name):
        """Process file in SIC format."""
        logging.info('Processing file %s as SIC format', file_name)
        base_file_name = os.path.basename(file_name)
        year = 2000 + int(base_file_name[11:13])
        month = int(base_file_name[13:15])
        the_array = Script.load_csv(file_name)
        the_array = the_array[the_array[SIC_TIPO1].isin(['L', 'L_D', 'R'])]
        the_array = the_array.pivot_table(
            values=[SIC_MEDIDAHORARIA2],
            index=[SIC_HORA_MENSUAL, SIC_NOMBRE_BARRA],
            aggfunc=np.sum).reset_index()
        date_features = dates_util.get_complete_date_features(
            year * np.ones(the_array.shape[0]),
            month * np.ones(the_array.shape[0]),
            hour_in_month_array=the_array[SIC_HORA_MENSUAL])
        date_features[OUTPUT_NODE] = the_array[SIC_NOMBRE_BARRA]
        date_features[OUTPUT_VALUE] = the_array[SIC_MEDIDAHORARIA2]
        return date_features

    def process_sing_file(self, file_name):
        """Process file in SIC format."""
        logging.info('Processing file %s as SING format', file_name)
        the_array = Script.load_csv(file_name)
        tapoff_array = pd.Series(['TAPOFF'] * len(the_array))
        aux_array = the_array[
            (the_array[SING_IDTIPOMEDIDA] == 'AUXILIAR') &
            (the_array[SING_ISINYECCION] == 0) &
            the_array[SING_IDUSOMEDIDA].isin(['BAL', 'BAL-COMP', 'COMP']) &
            (the_array[SING_IDNODOREF].isnull() |
             (the_array[SING_IDNODOREF].str.find('SSAA') == -1)) &
            (the_array[SING_IDTRAMO].str.split(pat=' - ', expand=True)[1] !=
             the_array[SING_IDNODOMEDIDA]) &
            (the_array[SING_IDTRAMO].str.split(pat=' - ', expand=True)[1] !=
             tapoff_array.str.cat(the_array[SING_IDNODOMEDIDA])) &
            ((the_array[SING_IDTRAMO] != self._sing_mock_tramo_ref[0]) |
             (the_array[SING_IDNODOREF] != self._sing_mock_tramo_ref[1])) &
            (~(the_array[SING_IDTRAMO].isin(self._sing_mock_tramos))) &
            the_array[SING_IDNODOMEDIDA].isin(self._sing_consider_bars)]
        aux_array = aux_array.pivot_table(
            values=[SING_VALORKWH],
            index=[SING_FECHAMEDIDA, SING_PERIODOMEDIDA, SING_IDNODOMEDIDA],
            aggfunc=np.sum).reset_index()
        the_array = the_array[
            (the_array[SING_IDTIPOMEDIDA] == 'COMERCIAL') &
            (the_array[SING_ISINYECCION] == 0) &
            the_array[SING_IDUSOMEDIDA].isin(['BAL', 'BAL-COMP']) &
            (the_array[SING_IDNODOREF].isnull() |
             (the_array[SING_IDNODOREF].str.find('SSAA') == -1)) &
            (the_array[SING_IDTRAMO].str.split(pat=' - ', expand=True)[1] !=
             the_array[SING_IDNODOMEDIDA]) &
            (the_array[SING_IDTRAMO].str.split(pat=' - ', expand=True)[1] !=
             tapoff_array.str.cat(the_array[SING_IDNODOMEDIDA])) &
            ((the_array[SING_IDTRAMO] != self._sing_mock_tramo_ref[0]) |
             (the_array[SING_IDNODOREF] != self._sing_mock_tramo_ref[1])) &
            (~(the_array[SING_IDTRAMO].isin(self._sing_mock_tramos))) &
            the_array[SING_IDNODOMEDIDA].isin(self._sing_consider_bars)]
        the_array = the_array.pivot_table(
            values=[SING_VALORKWH],
            index=[SING_FECHAMEDIDA, SING_PERIODOMEDIDA, SING_IDNODOMEDIDA],
            aggfunc=np.sum).reset_index()
        the_array = the_array.merge(
            aux_array, how='outer',
            on=[SING_FECHAMEDIDA, SING_PERIODOMEDIDA, SING_IDNODOMEDIDA])
        first_index = '{}_x'.format(SING_VALORKWH)
        second_index = '{}_y'.format(SING_VALORKWH)
        the_array[SING_VALORKWH] = (
            the_array[first_index].fillna(0.0) *
            (~(the_array[first_index].isnull())) +
            the_array[second_index].fillna(0.0) *
            the_array[second_index].isnull())
        year_array = [int('20{}'.format(row[SING_FECHAMEDIDA][6:8]))
                      for _, row in the_array.iterrows()]
        month_array = [int(row[SING_FECHAMEDIDA][:2])
                       for _, row in the_array.iterrows()]
        day_array = [int(row[SING_FECHAMEDIDA][3:5])
                     for index, row in the_array.iterrows()]
        hour_array = [row[SING_PERIODOMEDIDA]
                      for index, row in the_array.iterrows()]
        date_features = dates_util.get_complete_date_features(
            year_array, month_array, day_array=day_array,
            hour_array=hour_array)
        date_features[OUTPUT_NODE] = [SING_NODES[row[SING_IDNODOMEDIDA]]
                                      for _, row in the_array.iterrows()]
        date_features[OUTPUT_VALUE] = the_array[SING_VALORKWH]
        return date_features

    def process_csv_file(self, file_name):
        """Process given CSV file."""
        base_file_name = os.path.basename(file_name)
        if base_file_name.startswith('valorizado'):
            return Script.process_sic_file(file_name)
        if base_file_name.startswith('balance'):
            return self.process_sing_file(file_name)
        logging.warning('Not processing %s, unknown source', file_name)
        return None


def main():
    """Main execution point."""
    parser = argparse.ArgumentParser(
        description='Read raw data files and convert them into input format.')
    parser.add_argument(
        '--directory', default='.', help='directory where files are located')
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    Script(args.directory).run()


if __name__ == '__main__':
    main()
