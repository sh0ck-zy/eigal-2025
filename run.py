from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"""
    ################################################
    
    🚀 Aplicação iniciada: http://localhost:{port}/
    
    NAU Industrial - Transformação Digital da Gráfica
    
    ################################################
    """)
    app.run(debug=True, host='0.0.0.0', port=port) 