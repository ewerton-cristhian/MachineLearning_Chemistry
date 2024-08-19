from flask import Flask, render_template, request, jsonify, send_from_directory
from lib.descriptor_gen import DescriptorGen
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates')

def predict_CYP3A4(molecule_smiles):
    desc_gen = DescriptorGen()
    desc = desc_gen.from_smiles(molecule_smiles)
    desc = np.stack(desc).reshape(1, -1)

    path_model = 'models/model_standard.pkl'
    #path_model = 'models/model_resampled.pkl'

    model = joblib.load(path_model)
    pred = model.predict(desc)[0]
    pred_prob = model.predict_proba(desc)[0]

    #['Inhibitor', 'Inactive', 'Activator']
    #[2, 1, 0]

    print(pred_prob)

    if pred == 0:
        prob = np.round(pred_prob[0]*100,2)
        result = f'Class {pred} | Activator ({prob})%'

    if pred == 1:
        prob = np.round(pred_prob[1]*100,2)
        result = f'Class {pred} | Inactive ({prob})%'

    if pred == 2:
        prob = np.round(pred_prob[2]*100,2)
        result = f'Class {pred} | Inhibitor ({prob})%'

    return result


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/ketcher', methods=['GET'])
def ketcher_iframe():
   return render_template('ketcher/index.html')

@app.route('/submit', methods=['POST']) #
def submit():
    # Obter os dados da solicitação
    dados = request.get_json()
    molecule_smiles = dados.get('variavel')
    
    result = predict_CYP3A4(molecule_smiles)

    # Exibir o dado recebido no console do servidor
    print(f"Variável recebida: {molecule_smiles}")
    print(f"Classe de atividade em CYP3A4: {result}")
    
    # Retornar uma resposta JSON
    return jsonify({'response': f'{result}'})


if __name__ == "__main__":
    app.run(port=3000, debug=True)



''' 
@app.route('/js/getMolecule.js', methods=['GET'])
def get_molecule_js():
    return send_from_directory('static/js', 'getMolecule.js')



'''